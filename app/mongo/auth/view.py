from . import auth
from flask import current_app, session
from pymongo import MongoClient
from app.lastfm.forms import LoginForm
import app

@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    global db_client
    app.db_client = MongoClient('localhost', 27017)
    database = app.db_client.test
    user_data = database.users.find_one({'_id' : form.id.data})
    if user_data:
        session['user'] = form.id.data
    return str(user_data)


@auth.route('/logout')
def logout():
    del(session['user'])
    return "Hello world"