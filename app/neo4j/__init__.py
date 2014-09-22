from flask import Blueprint

neo4j = Blueprint('neo4j', __name__)
from . import view
