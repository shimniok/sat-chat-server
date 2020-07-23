import os
from flask_sqlalchemy import SQLAlchemy
from config import create_config
from flask import Flask

db = SQLAlchemy()

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    #app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object(create_config(env = os.environ['APP_SETTINGS']))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # setup login manager and initialize for this app
    from auth import login_manager
    login_manager.init_app(app)

    with app.app_context():
        from models import db, init_db
        init_db(app)

        from auth import auth_bp
        app.register_blueprint(auth_bp)

        from main import main_bp
        app.register_blueprint(main_bp)

        from message import message_bp
        app.register_blueprint(message_bp)

        from user import user_bp
        app.register_blueprint(user_bp)

        from device import device_bp
        app.register_blueprint(device_bp)

        from rockblock import rockblock_bp
        app.register_blueprint(rockblock_bp)

        if app.config['DEVELOPMENT']:
            from loopback import loopback_bp as loopback_blueprint
            app.register_blueprint(loopback_blueprint)

        return app
