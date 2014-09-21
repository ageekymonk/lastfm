from flask import Blueprint

artists = Blueprint('mongo.artists', __name__)
from . import view

