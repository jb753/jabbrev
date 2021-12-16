"""Testing a basic implementation of Journal abbreviations."""

import sys
import string

PREPOSITIONS = ['of', 'the', 'and', 'for', 'a', 'in', 'on']

# grep -v "n.a." ltwa_20210702.csv | sed -n 's/"\(.*\)";"\(.*\)";".*eng.*"/\1;\2/p' | iconv -f UTF-8 -t ASCII//TRANSLIT > ltwa_eng.csv

class WordList():
    """Encapsulate a list of words."""

    def __init__(self, word_list_file):
        """Read and parse a word list file to make this class."""

        # Read word list
        with open(word_list_file) as f:
            word_list_raw = f.readlines()

        # Preallocate dictionarys for the possible types of entry in the list
        self.abbreviations = {}
        self.prefix = {}
        self.suffix = {}
        self.non_abbreviations = []

        # Loop over lines and split the words
        for line in word_list_raw:
            word_long, word_short = line.strip().casefold().split(";")

            # If the short form is an acronym, remove spaces
            if " " in word_short:
                if 3*word_short.count(".")-1 == len(word_short):
                    word_short = word_short.replace(" ","")

            # Check for non-abbreviations
            if word_short == "n.a.":
                self.non_abbreviations.append(word_long)
            # Check for suffixes
            elif word_long[0] == "-":
                self.suffix[word_long[1:]] = word_short[1:]
            # Check for prefixes
            elif word_long[-1] == "-":
                self.prefix[word_long[:-1]] = word_short
            # Otherwise this is an abberviation
            else:
                self.abbreviations[word_long] = word_short

        # Store the minimum prefix and suffix lengths
        self.prefix_length, self.suffix_length = [
                min([len(w) for w in wl]) for wl in [self.prefix, self.suffix]
                ]

        # Store the maximum number of words in a multi-word abbreviations
        self.non_abbrev_multiword_length, self.abbrev_multiword_length = [
            max([w.count(" ") for w in wl]) for wl in
            [self.abbreviations, self.non_abbreviations]
            ]

    def check_prefix(self, word):
        """Check if the current word has an abbreviatable prefix."""
        # This calls for some thought. Doing a substring comparison with every
        # item in the dictionary would be expensive. Instead, we trim letters
        # from the end of the string and and check if what remains is "in" the
        # prefix dictionary. This requires at most len(word)-prefix_length
        # checks.
        for trim_stop in range(len(word),self.prefix_length-1,-1):
            word_trim = word[:trim_stop]
            if word_trim in self.prefix:
                return self.prefix[word_trim]
        return False

    def check_suffix(self, word):
        """Check if the current word has an abbreviatable suffix."""
        # Like check_prefix, we trim off the front of the string and see if any
        # of them match
        for trim_start in range(1,len(word)-self.suffix_length+1):
            word_trim = word[trim_start:]
            if word_trim in self.suffix:
                return word[:trim_start] + self.suffix[word_trim]
        return False

    def process_word(self, word):
        """Perform all checks and return any abbreviations possible."""

        # If all caps, return unchanged
        if word.strip(string.punctuation).isupper():
            return word

        # From now on, we assume case is not important
        word_lower = word.casefold()

        # Handle no abbreviation or verbatim abbreviation cases
        if word_lower in self.non_abbreviations:
            return word.title()
        elif word_lower in self.abbreviations:
            return self.abbreviations[word_lower].title()

        # Check if any prefixes are matched
        prefix = self.check_prefix(word_lower)
        if prefix:
            return prefix.title()

        # Check if any suffices are matched
        suffix = self.check_suffix(word_lower)
        if suffix:
            return suffix.title()

        # Otherwise, return unchanged
        return word.capitalize()

    def join_multiwords(self, words):
        """Take a list of words and join any that are valid abbreviations."""
        # Attempt to join abbreviations up to four words long
        for num_words in range(4,1,-1):
            if len(words) >= num_words:
                for start in range(0,len(words)-(num_words-1)):
                    trial_multi = " ".join(words[start:(start+num_words)]).casefold()
                    if (trial_multi in self.abbreviations
                            or trial_multi in self.non_abbreviations):
                        words[start] = trial_multi
                        words[start+1:(start+num_words)] = ""
                        break

def abbreviate(title_str, word_list):
    """Take a long title string and abbreviate it."""

    title_long = title_str.split(" ")

    word_list.join_multiwords(title_long)

    # Do not abbreviate single-word titles
    if len(title_long) == 1:
        title_short = title_long[0].capitalize()
    else:
        # Now, process each word individually
        title_short_words = [word_list.process_word(w.strip(',')) for w in title_long]

        # Omit prepositions unless they occur at end
        for i, w in enumerate(title_short_words[:-1]):
            if w.casefold() in PREPOSITIONS:
                title_short_words[i] = ""

        title_short = " ".join(
                [w for w in title_short_words if not w == ""]
            )
    return title_short


if __name__=="__main__":

    # Get the abbreviation dictionary from word list file
    word_list = WordList("ltwa_eng.csv")

    # Collect arguments from standard input or sys.argv
    if not sys.stdin.isatty():
        for line in sys.stdin:
            print(abbreviate(line.strip('\n'), word_list))
    else:
        if len(sys.argv)==1:
            print('Usage: jabbrev.py TITLE')
        else:
            print(abbreviate(" ".join([w for w in sys.argv[1:]]), word_list))
