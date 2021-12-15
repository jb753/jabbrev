from flask import Flask, render_template, request
import jabbrev

app = Flask(__name__)

word_list = jabbrev.WordList('ltwa_eng.csv')

@app.route('/<journal>')
def abbreviate(journal):
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
