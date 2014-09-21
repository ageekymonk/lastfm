from flask import session, redirect, render_template, url_for, g
from . import users
from app.lastfm.forms import LoginForm, SearchForm
import app

@users.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@users.route('/')
def index():
    if not session['user']:
        return redirect(url_for('/'))
    database = app.db_client.test
    user_data = database.users.find_one({'_id' : session['user']})
    friends_data = database.users.find({'_id' : {"$in" : user_data['friends']}})
    return render_template('mongo/users/users.html',user=user_data, friends=friends_data)

@users.route('/profile/<id>')
def view(id):
    database = app.db_client.test
    user_data = database.users.find_one({'_id' : id})
    friends_data = [data for data in database.users.find({'_id' : {"$in" : user_data['friends'], "$nin": [id]}})]

    reco_artist_list = []
    reco_type_info = {}
    for friend_data in friends_data:
        for artist in friend_data['artists']:
            reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + 1

    reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get)[0:5])

    reco_type_info = {}
    for friend_data in friends_data:
        for artist in friend_data['artists']:
            reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + artist['playcount']

    reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get)[0:5])
    reco_artist_info = [data for data in database.artists.find({'_id' : {"$in" : reco_artist_list}})]

    return render_template('mongo/users/users.html',user=user_data, friends=friends_data, reco_artist_info=reco_artist_info)