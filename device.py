## DEVICE API ############################################################################################

from flask import Blueprint, jsonify, request, abort
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import Device, db

device = Blueprint('device', __name__, url_prefix='/api')

# TODO: admin role can interact with anything

@device.before_request
def device_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401

@device.route('/device', methods=['get'])
def device_get():
    devices = Device.query.all()

    return jsonify([m.to_dict() for m in devices])

@device.route('/device', methods=['post'])
def devices_post():
    if not request.json:
        abort(400)
    try:
        dev = Device()
        #dev.owner_id = current_user,
        dev.imei = request.json['imei'],
        dev.username = request.json['username'],
        dev.password = request.json['password']

    except Exception as e:
        return "Bad request: {}".format(e), 400

    db.session.add(dev)
    db.session.commit()

    return jsonify(dev.to_dict())

# PUSH

# DELETE
