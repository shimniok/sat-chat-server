## MESSAGE API ############################################################################################

from flask import Blueprint, jsonify
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import Message

message = Blueprint('message', __name__, url_prefix='/api')

@message.before_request
def message_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401

@message.route('/message', methods=['get'])
def messages_get():
    list = []
    msgs = Message.query.order_by(Message.momsn).all()
    return jsonify([m.to_dict() for m in msgs])


@message.route('/message/<id>')
def message_get(id=-1):
    if not current_user.is_authenticated:
        return "Unauthorized", 401

    msg = Message.query.filter_by(id = id).first_or_404()

    return jsonify(msg.to_dict())

@message.route('/message/<id>', methods=['delete'])
def message_delete(id=-1):
    if not current_user.is_authenticated:
        return "Unauthorized", 401

    msg = Message.query.filter_by(id = msg_id).first_or_404()
    db.session.delete(msg)
    db.session.commit()

    return jsonify(msg.to_dict())
