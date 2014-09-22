from . import auth
from flask import current_app, session, redirect, url_for
from py2neo import neo4j
from py2neo import cypher
from app.lastfm.forms import LoginForm
import app

@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    global db_client
    app.graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    user_data, user_metadata = cypher.execute(app.graph_db, "MATCH (n:USER {{ id : {0}}}) RETURN (n)".format(int(form.id.data)))

    if user_data[0][0]['id']:
        session['user'] = int(form.id.data)
        return redirect('/')
    else:
        return redirect('/')


@auth.route('/logout')
def logout():
    del(session['user'])
    return redirect('/')