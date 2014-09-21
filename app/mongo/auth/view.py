from . import auth
from flask import current_app, session, redirect, url_for
from pymongo import MongoClient
from app.lastfm.forms import LoginForm
import app

@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    global db_client
    app.db_client = MongoClient('localhost', 27017)
    database = app.db_client.music
    user_data = database.users.find_one({'_id' : int(form.id.data)})
    if user_data:
        session['user'] = int(form.id.data)
        return redirect('/')
    else:
        return redirect('/')


@auth.route('/logout')
def logout():
    del(session['user'])
    return redirect('/')