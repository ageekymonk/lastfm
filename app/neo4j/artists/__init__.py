from flask import Blueprint

artists = Blueprint('neo4j.artists', __name__)
from . import view

