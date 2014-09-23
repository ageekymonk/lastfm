from flask import session, redirect, render_template, url_for, g, request
from . import users
from app.lastfm.forms import LoginForm, SearchForm
import app
import random
from itertools import chain
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

    # Recommend based on number of friends listen to the artist
    reco_artist_info = []
    match_data, metadata = cypher.execute(app.graph_db, "match (m:USER{{id:{0}}})-[:FRIEND]->(n:USER)-[l:LISTENS]->(o:ARTIST) "
                                                        "where not m-[:LISTENS]->o return o,count(l),sum(l.count)  "
                                                        "order by count(l) desc".format(id))

    # Recommend based on number of listen count among the friends
    reco_artist_info.extend(map(lambda x: x[0], sorted(match_data, key=lambda x: x[1])[:5]))
    # Recommend based on number of listen count among the friends
    reco_artist_info.extend(map(lambda x: x[0], sorted(match_data, key=lambda x: x[2])[:5]))

    # Recommend based on random tag from your list
    match_data, metadata = cypher.execute(app.graph_db, "match (m:USER{{id:{0}}})-[l:TAGS]->(n:ARTIST) "
                                                        "return collect(l.tags);".format(id))
    tag_list = list(chain.from_iterable(match_data[0][0]))
    if len(tag_list):
        random_tag = random.choice(tag_list)

    match_data, metadata = cypher.execute(app.graph_db, "match (m:USER)-[l:`{0}`]->(n:ARTIST)"
                                                        "<-[r:LISTENS]-(o:USER) return n,count(r) "
                                                        "order by count(r) desc limit 5;".format(random_tag))

    for datum in match_data:
        print datum[0]
        reco_artist_info.append(datum[0])

    return render_template('neo4j/users/users.html',user=user_data, friends=friends_data, reco_artist_info=reco_artist_info)

@users.route('/befriend', methods=["POST"])
def befriend():
    id = int(request.form['friend'])
    tag_data,metadata=cypher.execute(app.graph_db, "match (m:USER{{id:{0}}}),(n:USER{{id:{1}}}) "
                                                   "create unique m-[r:FRIEND]->n".format(session['user'], id))
    return redirect(url_for('neo4j.users.view',id=session['user']))