## MESSAGE API ############################################################################################

from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import Message, db

endpoint = '/api/message'

message_bp = Blueprint('message', __name__)

@message_bp.before_request
def message_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401


@message_bp.route(endpoint, methods=['get'])
def messages_get():
    messages = Message.query.order_by(Message.momsn).all()
    return jsonify([m.to_dict() for m in messages])


@message_bp.route(endpoint + '/since', methods=['get'])
def message_since_bogus():
    return jsonify([])


# Get messages since the specified momsn
@message_bp.route(endpoint + '/since/<momsn>', methods=['get'])
def messages_since(momsn):
    momsn = int(momsn)
    messages = Message.query.order_by(Message.momsn).all()

    return jsonify([m.to_dict() for m in messages if m.momsn > momsn])


@message_bp.route(endpoint + '/<id>', methods=['get'])
def message_get(id=-1):

    message = Message.query.filter_by(id = id).first_or_404()

    return jsonify(message.to_dict())


@message_bp.route(endpoint, methods=['post'])
def message_post():
    try:
        data = request.json
        message = Message(
            #imei = data['imei'],
            momsn = data['momsn'],
            sender_id = current_user,
            transmit_time = data['transmit_time'],
            time = data['time'],
            iridium_latitude = float(data['iridium_latitude']),
            iridium_longitude = float(data['iridium_longitude']),
            iridium_cep = data['iridium_cep'],
            message = data['message']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())

    except Exception as e:
        return "Error: {}".format(e), 400


@message_bp.route(endpoint + '/<id>', methods=['delete'])
def message_delete(id=-1):

    msg = Message.query.filter_by(id = id).first_or_404()
    db.session.delete(msg)
    db.session.commit()

    return jsonify(msg.to_dict())
