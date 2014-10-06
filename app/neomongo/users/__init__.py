from flask import Blueprint

users = Blueprint('neomongo.users', __name__)
from . import view

