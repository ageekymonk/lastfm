from flask import render_template, session, redirect, url_for, g, request
from . import artists
import app
from app.lastfm.forms import LoginForm, SearchForm

@artists.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@artists.route('/')
def index():
    database = app.db_client.music
    user_data = database.users.find_one({'_id' : session['user']})
    return render_template('mongo/artists/artists.html', user=user_data)

@artists.route('/view/<id>')
def view(id):
    id = int(id)
    database = app.db_client.music
    user_data = database.users.find_one({'_id' : session['user']})
    artist_data = database.artists.find_one({'_id' : id})
    tags_data_raw = database.users.find({'artists.artist' : id}, {'artists.$' : 1})
    tag_list = set({})
    listeners = 0
    played = 0
    user_tag_list = []
    for artist in user_data['artists']:
        print artist['artist']
        if int(artist['artist']) == id:
            print id
            if artist.has_key('tag'):
                for tag in artist['tag']:
                    user_tag_list.append(tag)
            break

    for tags_datum in tags_data_raw:
        if tags_datum['artists'][0]['playcount']:
            listeners = listeners + 1
            played = played + int(tags_datum['artists'][0]['playcount'])
        if tags_datum['artists'][0].has_key('tag'):
            for tag in tags_datum['artists'][0]['tag']:
                tag_list.add(tag)

    user_tag_list.extend(list(tag_list))
    # Top Friends who has played the artist
    friends_list = []
    for tags_datum in tags_data_raw:
        if tags_datum['_id'] in user_data['friends']:
            friends_list.append(tags_datum)
    return render_template('mongo/artists/view.html', artist=artist_data, tag_list=user_tag_list, played = played, listeners=listeners, friends_list=friends_list)

@artists.route('/listen/<id>', methods=["POST"])
def listen(id):
    id = int(id)
    database = app.db_client.music
    database.users.update({'_id' : session['user'], 'artists.artist' : id}, {"$inc" : {'artists.$.playcount' : 1}})
    return redirect(url_for('mongo.artists.index'))

@artists.route('/tag/<id>', methods=["POST"])
def tag(id):
    id = int(id)
    database = app.db_client.music
    database.users.update({'_id' : session['user'], 'artists.artist' : id}, {"$addToSet" : {'artists.$.tag' : request.form['tags']}})
    return redirect(url_for('mongo.artists.view',id=id))

@artists.route('/search', methods=["POST"])
def search():
    print request.form['searchterm']
    database = app.db_client.music
    search_artists = database.artists.find({'name' : {"$regex" : '.*'+request.form['searchterm']+'.*', "$options" : 'i'}})
    artist_list = [artist for artist in  search_artists]
    return render_template('mongo/artists/search.html',artist_list=artist_list)