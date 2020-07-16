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

    return jsonify([d.to_dict() for d in devices])

@device.route('/device', methods=['post'])
def devices_post():
    if not request.json:
        abort(400)
    try:
        dev = Device()
        dev.imei = request.json['imei']
        dev.username = request.json['username']
        dev.password = request.json['password']

    except Exception as e:
        return "Bad request: {}".format(e), 400

    db.session.add(dev)
    db.session.commit()

    return jsonify(dev.to_dict())

@device.route('/device/<id>', methods=['put'])
def devices_put(id):
    if not request.json:
        abort(400)
    try:
        dev = Device.query.filter_by(id=id).first_or_404()
        dev.imei = request.json['imei']
        dev.username = request.json['username']
        dev.password = request.json['password']
        db.session.commit()

    except Exception as e:
        return "Bad request: {}".format(e), 400

    return jsonify(dev.to_dict())

# DELETE
