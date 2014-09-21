from flask import Blueprint

users = Blueprint('mongo.users', __name__)
from . import view

