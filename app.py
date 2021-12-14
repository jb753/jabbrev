from flask import Flask, render_template, request
import jabbrev

app = Flask(__name__)

word_list = jabbrev.WordList('ltwa_eng.csv')

@app.route('/',methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        long_title = request.form['long_title']
        short_title = jabbrev.abbreviate(long_title,word_list)
    else:
        short_title = ""
        long_title = ""

    return render_template(
            'index.html',
            short_title=short_title,
            long_title=long_title,
            )
