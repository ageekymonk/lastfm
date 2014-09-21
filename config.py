import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

class DevelopmentConfig(Config):
    SECRET_KEY = 't0ps3cr3t'
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production': ProductionConfig,
    'default' : DevelopmentConfig
}