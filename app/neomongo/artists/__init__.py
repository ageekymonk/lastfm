from flask import Blueprint

artists = Blueprint('neomongo.artists', __name__)
from . import view

