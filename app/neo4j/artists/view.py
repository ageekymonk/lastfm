from flask import render_template, session, redirect, url_for, g, request
from . import artists
import app
from app.lastfm.forms import LoginForm, SearchForm
from py2neo import neo4j
from py2neo import cypher

@artists.before_request
def before_request():
    g.login_form = LoginForm()
    g.search_form = SearchForm()

@artists.route('/')
def index():
    data, metadata = cypher.execute(app.graph_db, "MATCH (n:USER {{ id : {0}}}) RETURN (n)".format(int(session['user'])))
    match_data, metadata = cypher.execute(app.graph_db, "match (m:USER{{id:{0}}})-[l:LISTENS]"
                                                        "->(n:ARTIST) return n,l".format(session['user']))
    return render_template('neo4j/artists/artists.html', user=data[0], artist_data=match_data)

@artists.route('/view/<id>')
def view(id):
    id = int(id)
    user_data, user_metadata = cypher.execute(app.graph_db, "match (n:USER {{ id : {0} }})-[l:TAGS]->"
                                                            "(m:ARTIST {{ id  : {1} }}) RETURN n,l,m".format(session['user'], id))
    tag_list = []
    for row in user_data:
        tag_list.extend(row[1]['tags'])

    artist_data, metadata = cypher.execute(app.graph_db, "match (n:ARTIST {{ id : {0} }}) RETURN n".format(id))
    listen_data,metadata = cypher.execute(app.graph_db, "match (n:ARTIST {{id : {0}}})<-[l:LISTENS]-"
                                               "(m:USER) return l;".format(id))

    listeners = len(listen_data)
    playcount = 0
    for datum in listen_data:
        playcount = playcount + datum[0]['count']

    tag_data, metadata = cypher.execute(app.graph_db, "match (n:USER)-[l:TAGS]->(m:ARTIST {{ id  : {0} }}) where n.id <> {1} RETURN n,l,m".format(id, session['user']))
    for datum in tag_data:
        tag_list.extend(datum[1]['tags'])

    #TODO: Top Friends who has played the artist
    return render_template('neo4j/artists/view.html', artist=artist_data[0][0], tag_list=tag_list, played = playcount, listeners=listeners, friends_list=[])

@artists.route('/listen/<id>', methods=["POST"])
def listen(id):
    id = int(id)
    listen_data,metadata=cypher.execute(app.graph_db, "match (n:USER{{id :{0}}}),(m:ARTIST{{id:{1}}}) "
                                        "create unique n-[r:LISTENS]->m set r.count = coalesce(r.count,0)+1;".format(session['user'],id))
    return redirect(request.referrer)

@artists.route('/tag/<id>', methods=["POST"])
def tag(id):
    id = int(id)
    tag_data,metadata=cypher.execute(app.graph_db, "match (m:USER{{id:{0}}}),(n:ARTIST{{id:{1}}}) "
                                                   "create unique m-[r:TAGS]->n set r.tags = "
                                                   "case when not (has (r.tags)) then [] when not '{2}' in r.tags "
                                                   "then r.tags + '{2}' else r.tags end;".format(session['user'], id,request.form['tags']))

    tag_data,metadata = cypher.execute(app.graph_db, "MATCH (n:USER {{id: {0} }}), (m: ARTIST {{id: {1}}}) "
                        "CREATE unique (n)-[:`{2}`]->m RETURN n".format(session['user'],id,request.form['tags']))

    #TODO Add another query to create a new relationship with the tag
    return redirect(url_for('neo4j.artists.view',id=id))

@artists.route('/search', methods=["POST"])
def search():
    data, metadata = cypher.execute(app.graph_db, "match (n:ARTIST) where n.name =~ '(?i).*{0}.*' "
                                                  "return (n) limit 10;".format(request.form['searchterm']))
    artist_list = []
    for row in data:
        artist_list.append(row[0])
    return render_template('neo4j/artists/search.html',artist_list=artist_list)