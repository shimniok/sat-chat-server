from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app import app

main = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses
#TODO angularjs login_post
#TODO remove signup, add user administration page
#TODO implement SMS alerting

@main.route('/')
@login_required
def index():
    return render_template("index.html")

@main.route('/admin')
@login_required
def admin():
    return "admin"

@main.route('/admin/messages')
@login_required
def admin_messages():
    return render_template("admin.html")

@main.route('/admin/users')
@login_required
def admin_users():
    return "admin_users"
