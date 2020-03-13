import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    print(os.environ['IMEI'])
    SECRET_KEY = os.environ['SECRET_KEY']
    IMEI = os.environ['IMEI']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
