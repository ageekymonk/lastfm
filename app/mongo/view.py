from flask import render_template
from . import mongo
from app import db_client

@mongo.route('/')
def index():
    return "Hello world"
