import os
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
    return config

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
    SEND_FILE_MAX_AGE_DEFAULT = 0 


class DevelopmentConfig(Config):
    LOOPBACK_ENABLED = True
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
