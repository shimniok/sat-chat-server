from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses

@main.route('/')
@login_required
def index():
    return render_template("index.html", name=current_user.name)
