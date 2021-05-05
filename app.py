import os
from flask_sqlalchemy import SQLAlchemy
from config import create_config
from flask import Flask
from json_parser import dt_fmt

db = SQLAlchemy()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config == None:
        my_config = create_config(env=os.environ['APP_SETTINGS'])
    else:
        my_config = test_config

    app.config.from_object(my_config)

    # setup login manager and initialize for this app
    from api.auth import login_manager
    login_manager.init_app(app)

    with app.app_context():
        from api.models import init_db
        init_db(app)

        from json_parser import CustomJSONEncoder
        app.json_encoder = CustomJSONEncoder

        from api.auth import auth_bp
        app.register_blueprint(auth_bp)

        from main import main_bp
        app.register_blueprint(main_bp)

        from api.message import message_bp
        app.register_blueprint(message_bp)

        from api.user import user_bp
        app.register_blueprint(user_bp)

        from api.device import device_bp
        app.register_blueprint(device_bp)

        from api.rockblock import rockblock_bp
        app.register_blueprint(rockblock_bp)

        if app.config['DEVELOPMENT']:
            from api.loopback import loopback_bp
            app.register_blueprint(loopback_bp)

        return app
