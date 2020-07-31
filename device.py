## DEVICE API ############################################################################################

from flask import Blueprint, jsonify, request, abort
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from models import Device
from models import db

endpoint = '/api/device'

device_bp = Blueprint('device', __name__)

# TODO: admin role can interact with anything

@device_bp.before_request
def device_before():
    print("device_before()")
    if not current_user.is_authenticated:
        abort(401)


@device_bp.route(endpoint, methods=['get'])
def device_get():
    devices = Device.query.all()

    return jsonify([d.to_dict() for d in devices])


@device_bp.route(endpoint, methods=['post'])
def devices_post():
    if not request.json:
        abort(400)
    try:
        dev = Device(
            imei = request.json['imei'],
            username = request.json['username'],
            password = request.json['password'],
            owner_id = current_user.id
        )
        db.session.add(dev)
        db.session.commit()
    except Exception as e:
        print("Error: {}".format(e))
        return "Bad request: {}".format(e), 400

    return jsonify(dev.to_dict())



@device_bp.route(endpoint+'/<id>', methods=['put'])
def device_put(id):
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


@device_bp.route(endpoint+'/<id>', methods=['delete'])
def device_del(id):
    try:
        dev = Device.query.filter_by(id = id).first_or_404()
        db.session.delete(dev)
        db.session.commit()
    except Exception as e:
        return "Bad request: {}".format(e), 400

    return jsonify(dev.to_dict())
