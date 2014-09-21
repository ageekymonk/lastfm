import os
from app import create_app
from flask.ext.script import Manager
from flask import url_for


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()