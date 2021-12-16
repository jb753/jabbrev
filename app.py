from flask import Flask, render_template, request
import jabbrev
import os
from datetime import datetime

app = Flask(__name__)

word_list = jabbrev.WordList('ltwa_eng.csv')

def log(query):
    """Record query to a rotated log file."""

    # Select log file name based on current year-month
    now = datetime.now()
    log_file = "log/log-%d-%d.txt" % (now.year, now.month)
    log_string = "%s %s\n" % (now.isoformat(), query)

    with open(log_file,'a+') as f:
        f.write(log_string)

@app.route('/<journal>')
def abbreviate(journal):
    log(journal)
    short_title = jabbrev.abbreviate(journal,word_list)
    return render_template(
            'index.html',
            short_title=short_title,
            long_title=journal,
            )

@app.route('/')
def index():

    return render_template(
            'index.html',
            short_title="",
            long_title="",
            )
