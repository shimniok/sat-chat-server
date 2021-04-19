from flask import Blueprint, render_template
from flask_login import current_user, login_required
#from api.auth import admin_required

main_bp = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses
#TODO implement SMS alerting
#TODO evaluate flask_login security

@main_bp.route('/')
def index():
    return render_template("index.html")
