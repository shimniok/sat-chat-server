from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import Message, User
from app import app

main = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses

@main.route('/')
@login_required
def index():
    messages = Message.query.order_by(Message.momsn).all()

    return render_template("index.html",
        my_name=current_user.name, my_id=current_user.id, messages=messages)
