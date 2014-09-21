from flask import Blueprint

auth = Blueprint('mongo.auth', __name__)
from . import view

