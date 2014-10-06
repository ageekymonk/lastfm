from flask import Blueprint

auth = Blueprint('neomongo.auth', __name__)
from . import view

