import os
from config import create_config
from flask import Flask

app = Flask(__name__)

#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(create_config(env = os.environ['APP_SETTINGS']))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# setup login manager and initialize for this app
from auth import login_manager
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

from message import message as message_blueprint
app.register_blueprint(message_blueprint)

from user import user as user_blueprint
app.register_blueprint(user_blueprint)

from device import device as device_blueprint
app.register_blueprint(device_blueprint)

from rockblock import rockblock as rockblock_blueprint
app.register_blueprint(rockblock_blueprint)

if app.config['DEVELOPMENT']:
    from loopback import loopback_bp as loopback_blueprint
    app.register_blueprint(loopback_blueprint)

from models import db
db.init_app(app)
