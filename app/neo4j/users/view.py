from flask import session, redirect, render_template, url_for, g, request
from . import users
from app.lastfm.forms import LoginForm, SearchForm
import app
import random
from py2neo import neo4j
from py2neo import cypher

@users.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@users.route('/')
def index():
    if not session['user']:
        return redirect(url_for('/'))
    match_data,metadata = cypher.execute(app.graph_db,"match (n:USER{{ id: {0}}})-[r:FRIEND]->(m:USER) return n,r,m".format(session['user']) )
    friends_data = []
    for datum in match_data:
        friends_data.append(datum[2])
    user_data = match_data[0][0]
    return render_template('neo4j/users/users.html',user=user_data, friends=friends_data)

@users.route('/profile/<id>')
def view(id):
    if not session['user']:
        return redirect(url_for('/'))
    id = int(id)
    match_data,metadata = cypher.execute(app.graph_db,"match (n:USER{{ id: {0}}})-[r:FRIEND]->(m:USER) return n,r,m".format(id) )
    friends_data = []
    for datum in match_data:
        friends_data.append(datum[2])
    user_data = match_data[0][0]

    reco_artist_info = []
    #
    # # Recommend based on number of friends listen to the artist
    # reco_artist_list = []
    # reco_type_info = {}
    # for friend_data in friends_data:
    #     for artist in friend_data['artists']:
    #         reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + 1
    #
    # reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get)[0:5])
    #
    # # Recommend based on number of listen count among the friends
    # reco_type_info = {}
    # for friend_data in friends_data:
    #     for artist in friend_data['artists']:
    #         reco_type_info[artist['artist']] = reco_type_info.get(artist['artist'],0) + artist['playcount']
    #
    # reco_artist_list.extend(sorted(reco_type_info, key=reco_type_info.get)[0:5])
    # # reco_artist_info = [data for data in database.artists.find({'_id' : {"$in" : reco_artist_list}})]
    # #
    # # Recommend based on tag list
    # tag_list = []
    # for artist in user_data['artists']:
    #     if artist.has_key('tag'):
    #         tag_list.extend(artist['tag'])
    #
    # random_tag = random.choice(tag_list)
    # artist_list = set({})
    # users_artist_data = database.users.find({'artists.tag' : random_tag, 'artists.artist' : {"$nin" : user_artist_list}},
    #                                          {"artists.$.artist" : 1})
    # unique_listener = {}
    # for datum in users_artist_data:
    #     for artist in datum['artists']:
    #         unique_listener[artist['artist']] = unique_listener.get(artist['artist'],0) + 1
    #
    # reco_artist_list.extend(sorted(unique_listener, key=unique_listener.get)[0:5])
    # reco_artist_info = [data for data in database.artists.find({'_id' : {"$in" : reco_artist_list}})]

    return render_template('neo4j/users/users.html',user=user_data, friends=friends_data, reco_artist_info=reco_artist_info)

@users.route('/befriend', methods=["POST"])
def befriend():
    id = int(request.form['friend'])
    tag_data,metadata=cypher.execute(app.graph_db, "match (m:USER{{id:{0}}}),(n:USER{{id:{1}}}) "
                                                   "create unique m-[r:FRIEND]->n".format(session['user'], id))
    return redirect(url_for('neo4j.users.view',id=session['user']))