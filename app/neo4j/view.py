from flask import render_template
from . import neo4j
from app import graph_db

@neo4j.route('/')
def index():
    return "Hello world"
