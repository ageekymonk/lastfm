from flask import Blueprint

neomongo = Blueprint('neomongo', __name__)
from . import view
