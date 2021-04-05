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

def get_my_device():
    return Device.query.filter_by(owner_id = current_user.id).first()

def get_device_by_imei(imei):
    return Device.query.filter_by(imei = imei).first_or_404()

@device_bp.route(endpoint, methods=['get'])
def device_get():
    device = get_my_device()

    if device == None:
        return jsonify([])
    else:
        return jsonify([device.to_dict()])


@device_bp.route(endpoint, methods=['post'])
def device_post():
    print("device_post (new)")
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



@device_bp.route(endpoint+'/<id>', methods=['post'])
def device_post_id(id):
    print("device_post (update)")
    if not request.json:
        abort(400)
    try:
        #TODO: ensure current_user owns this device!
        dev = Device.query.filter_by(id=id).first_or_404()
        if 'imei' in request.json:
            dev.imei = request.json['imei']
        if 'username' in request.json:            
            dev.username = request.json['username']
        if 'password' in request.json:        
            dev.password = request.json['password']
        db.session.commit()

    except Exception as e:
        return "Bad request: {}".format(e), 400

    return jsonify(dev.to_dict())



@device_bp.route(endpoint+'/<id>', methods=['delete'])
def device_del(id):
    try:
        #TODO: ensure current_user owns this device!
        dev = Device.query.filter_by(id = id).first_or_404()
        db.session.delete(dev)
        db.session.commit()
    except Exception as e:
        return "Bad request: {}".format(e), 400

    return jsonify(dev.to_dict())
