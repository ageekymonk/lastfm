from flask import render_template, g
from . import app
from app.lastfm.forms import LoginForm, SearchForm

@app.route('/')
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()