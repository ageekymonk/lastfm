from flask import Blueprint

auth = Blueprint('neo4j.auth', __name__)
from . import view

