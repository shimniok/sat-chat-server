## MESSAGE API ############################################################################################

from flask import Blueprint, jsonify, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from api.models import Message, Device, db
from api.device import get_my_device

endpoint = '/api/message'

message_bp = Blueprint('message', __name__)

@message_bp.before_request
def message_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401

# TODO: only allow access to messages to/from me


def get_latest_mt_message():
    my_dev = get_my_device()
    messages = Message.query.filter(
        Message.device_id == my_dev.id,
        Message.sender_id == current_user.id).order_by(Message.time.desc()).all()
    return messages[0]

def get_latest_mo_message():
    my_dev = get_my_device()
    messages = Message.query.filter(
        Message.device_id == my_dev.id,
        Message.sender_id == None).order_by(Message.time.desc()).all()    
    return messages[0]

@message_bp.route(endpoint, methods=['get'])
def messages_get():

    filter = True

    since_id = request.args.get('since_id')
    if since_id != None:
        print("since_id provided")
        latest = Message.query.filter(Message.id == since_id).first_or_404("No such message id")
        filter = Message.time > latest.time

    messages = Message.query.filter(filter).order_by(Message.time).all()

    return jsonify([m.to_dict() for m in messages])


@message_bp.route(endpoint + '/since/', methods=['get'])
def message_since_all():
    return messages_get()


# Get messages since the specified momsn
@message_bp.route(endpoint + '/since/<momsn>', methods=['get'])
def messages_since(momsn):
    momsn = int(momsn)
    # TODO: more efficient way to query database here?
    messages = Message.query.order_by(Message.momsn).all()

    return jsonify([m.to_dict() for m in messages if m.momsn > momsn])


@message_bp.route(endpoint + '/<id>', methods=['get'])
def message_get(id=-1):

    message = Message.query.filter_by(id=id).first_or_404()

    return jsonify(message.to_dict())


@message_bp.route(endpoint, methods=['post'])
def message_post():
    try:
        data = request.json

        # Lookup device by imei
        dev = Device.query.filter_by(imei=data['imei']).first_or_404()
        message = Message(
            device_id=dev['id'],
            momsn=data['momsn'],
            sender_id=current_user.id,
            transmit_time=data['transmit_time'],
            time=data['time'],
            iridium_latitude=float(data['iridium_latitude']),
            iridium_longitude=float(data['iridium_longitude']),
            iridium_cep=data['iridium_cep'],
            message=data['message']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())

    except Exception as e:
        return "Error: {}".format(e), 400


@message_bp.route(endpoint + '/<id>', methods=['delete'])
def message_delete(id=-1):

    msg = Message.query.filter_by(id=id).first_or_404()
    db.session.delete(msg)
    db.session.commit()

    return jsonify(msg.to_dict())
