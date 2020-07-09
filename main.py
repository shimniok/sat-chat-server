from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import Message, User

main = Blueprint('main', __name__, template_folder='templates')

#TODO log accesses

@main.route('/')
@login_required
def index():
    messages = Message.query.order_by(Message.momsn).all()

    msgs = []
    for m in messages:
        m_dict = m.to_dict()
        id = m_dict['sender']
        if id:
            user = User.query.filter_by(id = id).first()
            print(user)
            m_dict['name'] = user.name
        msgs.append(m_dict)

    return render_template("index.html", name=current_user.name, messages=msgs)
