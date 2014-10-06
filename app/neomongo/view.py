from flask import render_template
from . import neomongo

@neomongo.route('/')
def index():
    return "Hello world"
