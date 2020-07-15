from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app import app
from auth import admin_required

main = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses
#TODO angularjs login_post
#TODO remove signup, add user administration page
#TODO implement SMS alerting
#TODO evaluate flask_login security

@main.route('/')
def index():
    return render_template("index.html")
