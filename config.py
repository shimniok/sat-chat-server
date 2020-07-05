import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    IMEI = os.environ['IMEI']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    API_ENDPOINT = os.environ['API_ENDPOINT']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    LOOPBACK_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    LOOPBACK_ENABLED = True
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
