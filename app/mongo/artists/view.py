from flask import render_template, session, redirect, url_for, g
from . import artists
import app
from app.lastfm.forms import LoginForm, SearchForm

@artists.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@artists.route('/')
def index():
    database = app.db_client.test
    user_data = database.users.find_one({'_id' : session['user']})
    artists_list = [ data['artist'] for data in user_data['artists']]
    artist_data = [ x for x in database.artists.find({'_id' : {"$in" : artists_list }})]
    return render_template('mongo/artists/artists.html', user=user_data, artists=artist_data)

@artists.route('/view/<id>')
def view(id):
    database = app.db_client.test
    user_data = database.users.find_one({'_id' : session['user']})
    artist_data = database.artists.find_one({'_id' : id})
    tags_data_raw = database.users.find({'artists.artist' : id}, {'artists.$' : 1})
    tag_list = set({})
    listeners = 0
    played = 0
    for tags_datum in tags_data_raw:
        if tags_datum['artists'][0]['playcount']:
            listeners = listeners + 1
            played = played + int(tags_datum['artists'][0]['playcount'])
        if tags_datum['artists'][0].has_key('tag'):
            for tag in tags_datum['artists'][0]['tag']:
                tag_list.add(tag)

    # Top Friends who has played the artist
    friends_list = []
    for tags_datum in tags_data_raw:
        if tags_datum['_id'] in user_data['friends']:
            friends_list.append(tags_datum)
    return render_template('mongo/artists/view.html', artist=artist_data, tag_list=tag_list, played = played, listeners=listeners, friends_list=friends_list)

@artists.route('/listen/<id>', methods=["POST"])
def listen(id):
    database = app.db_client.test
    database.users.update({'_id' : session['user'], 'artists.artist' : id}, {"$inc" : {'artists.$.playcount' : 1}})
    return redirect(url_for('mongo.artists.index'))