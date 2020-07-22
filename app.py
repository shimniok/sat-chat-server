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
        from models import db
        db.init_app(app)

        from auth import auth_bp
        app.register_blueprint(auth_bp)

        from main import main_bp
        app.register_blueprint(main_bp)

        from message import message_bp
        app.register_blueprint(message_bp)

        from user import user as user_blueprint
        app.register_blueprint(user_blueprint)

        from device import device as device_blueprint
        app.register_blueprint(device_blueprint)

        from rockblock import rockblock as rockblock_blueprint
        app.register_blueprint(rockblock_blueprint)

        if app.config['DEVELOPMENT']:
            from loopback import loopback_bp as loopback_blueprint
            app.register_blueprint(loopback_blueprint)

        return app
