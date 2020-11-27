'''
open two files of different languages (preferably poetry), read them, and output a graph showing how they translate each other
'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def test_recipe():
    return render_template('index.html')
