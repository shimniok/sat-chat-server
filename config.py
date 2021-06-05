import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

def create_config(env):
    config = ()
    if env == 'Production':
        config = ProductionConfig()
    elif env == 'Development':
        config = DevelopmentConfig()
    elif env == 'Staging':
        config = StagingConfig()
    elif env == 'Testing':
        config = TestingConfig()
    else:
        print("Unrecognized APP_SETTINGS. Must be: Development|Staging|Production")
        raise Exception(
            "APP_SETTINGS must be: Development|Staging|Production")
    return config


class Config(object):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    API_ENDPOINT = os.environ['API_ENDPOINT']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    LOOPBACK_ENABLED = False
    REMEMBER_COOKIE_DURATION = timedelta(seconds=300)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    LOOPBACK_ENABLED = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOOPBACK_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
