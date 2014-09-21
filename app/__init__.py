from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config
from pymongo import MongoClient
from flask_cake import Cake

# change this to None once it is done
db_client = MongoClient('localhost', 27017)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    cake = Cake(app)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    from .lastfm import app as app_blueprint
    app.register_blueprint(app_blueprint)

    from .mongo import mongo as mongo_blueprint
    app.register_blueprint(mongo_blueprint, url_prefix='/mongo')

    from .mongo.artists import artists as mongo_artists_blueprint
    app.register_blueprint(mongo_artists_blueprint, url_prefix = '/mongo/artists')

    from .mongo.auth import auth as mongo_auth_blueprint
    app.register_blueprint(mongo_auth_blueprint, url_prefix='/mongo/auth')

    from .mongo.users import users as mongo_users_blueprint
    app.register_blueprint(mongo_users_blueprint, url_prefix='/mongo/users')

    return app