from flask import Blueprint

mongo = Blueprint('mongo', __name__)
from . import view
