from flask import Blueprint

users = Blueprint('neo4j.users', __name__)
from . import view

