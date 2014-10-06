from flask import session, redirect, render_template, url_for, g, request
from . import users
from app.lastfm.forms import LoginForm, SearchForm
import app
import random

@users.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@users.route('/')
def index():
    if not session['user']:
        return redirect(url_for('/'))
    database = app.db_client.music
    user_data = database.users.find_one({'_id' : session['user']})
    friends_data = database.users.find({'_id' : {"$in" : user_data['friends']}})
    return render_template('mongo/users/users.html',user=user_data, friends=friends_data)

@users.route('/profile/<id>')
def view(id):
    database = app.db_client.music
    id = int(id)
    user_data = database.users.find_one({'_id' : id})
    user_artist_list = [x['artist'] for x in user_data['artists']]
    friends_data = [data for data in database.users.find({'_id' : {"$in" : user_data['friends'], "$nin": [id]}})]

    # Recommend based on number of friends listen to the artist
    reco_artist_list = []
    reco_type_info = {}
    for friend_data in friends_data:
        for artist in friend_data['artists']:
            if artist['artist'] not in user_artist_list:
                reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + 1

    reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get, reverse=True)[0:5])

    # Recommend based on number of listen count among the friends
    reco_type_info = {}
    for friend_data in friends_data:
        for artist in friend_data['artists']:
            if artist['artist'] not in user_artist_list:
                reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + artist['playcount']


    reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get, reverse=True)[0:5])
    # reco_artist_info = [data for data in database.artists.find({'_id' : {"$in" : reco_artist_list}})]
    #
    # Recommend based on tag list
    tag_list = []
    for artist in user_data['artists']:
        if artist.has_key('tag'):
            tag_list.extend(artist['tag'])

    random_tag = random.choice(tag_list)
    artist_list = set({})
    users_artist_data = database.users.find({'artists.tag' : random_tag, 'artists.artist' : {"$nin" : user_artist_list}},
                                             {"artists.$.artist" : 1})
    unique_listener = {}
    for datum in users_artist_data:
        for artist in datum['artists']:
            if artist['artist'] not in user_artist_list:
                unique_listener[artist['artist']] = unique_listener.get(artist['artist'],0) + 1

    reco_artist_list.extend(sorted(unique_listener, key=unique_listener.get, reverse=True)[0:5])
    reco_artist_info = [data for data in database.artists.find({'_id' : {"$in" : reco_artist_list}})]

    return render_template('mongo/users/users.html',user=user_data, friends=friends_data, reco_artist_info=reco_artist_info)

@users.route('/befriend', methods=["POST"])
def befriend():
    database = app.db_client.music
    print {'_id' : session['user']}, {"$addToSet" : {'friends' : request.form['friend']}}
    database.users.update({'_id' : session['user']}, {"$addToSet" : {'friends' : int(request.form['friend'])}})
    return redirect(url_for('mongo.users.view',id=session['user']))