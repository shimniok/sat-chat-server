## SEND/RECEIVE API ########################################################################################

import requests
import binascii
import json
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from datetime import datetime, timezone
from models import Message, Device, db
from json_parser import dt_fmt

rockblock_bp = Blueprint('rockblock', __name__, url_prefix='/api', template_folder='templates')

# TODO: Convert to using message api versus databse

# Send data to Rock7
@rockblock_bp.route('/send', methods=['post'])
def send():
    if not current_user.is_authenticated:
        return "Unauthorized", 401

    try:
        #TODO: data = request.json
        data = json.loads(request.data.decode())
        text = data["message"]
        hex = binascii.b2a_hex(text.encode('utf-8'))
        print("send text={} hex={}".format(text, hex))
    except Exception as e:
        print("send(): problem preparing message {}".format(e))
        return "problem preparing message", 401

    data = {
        'username': current_app.config['USERNAME'],
        'password': current_app.config['PASSWORD'],
        'imei': current_app.config['IMEI'],
        'data': hex
    }
    r = requests.post(url = current_app.config['API_ENDPOINT'], data = data)

    # Parse return from request and return json
    #   Success: OK,12345678  --The number uniquely identifies your message.
    #   Failure: FAILED,15,Textual description of failure
    msg_bits = r.text.split(',')
    if not r.status_code == 200:
        result = {
            'status': 'FAILED',
            'error_number': r.status_code,
            'error_text': r.text
        }
    elif msg_bits[0] == 'OK':
        m = Message(
            sender_id=current_user.id,
            momsn=msg_bits[1],
            message=text,
            transmit_time=datetime.strftime(datetime.utcnow(), dt_fmt),
            time=datetime.strftime(datetime.utcnow(), dt_fmt)
        )
        #print('receive(): transmit_time: {}'.format(m.transmit_time))
        id = db.session.add(m)
        db.session.commit()
        result = {
            'status': msg_bits[0],
            'message': m.to_dict()
        }
    elif msg_bits[0] == 'FAILED':
        result = {
            'status': 'FAILED',
            'error_number': msg_bits[1],
            'error_text': msg_bits[2]
        }
    else:
        result = {
            'status': "FAILED",
            'error_number': "999",
            'error_text': r.text
        }
    if result['status'] == 'FAILED':
        print("{}".format(result.error_text))
    return jsonify(result)


# Receive data from Rock7
@rockblock_bp.route('/receive', methods=['get','post'])
def receive():

    parameters = [
        'imei', 'momsn', 'transmit_time', 'iridium_latitude', 'iridium_longitude', 'iridium_cep', 'data'
    ]

    # check for missing parameters
    missing = []
    for p in parameters:
        if not request.form.get(p):
            missing.append(p)
        else:
            print('receive: {}={}'.format(p, request.form.get(p)))
    if len(missing):
        print('receive(): bad request: missing: {}'.format(', '.join(missing)))
        return 'bad request: missing: {}'.format(', '.join(missing)), 400

    imei = request.form.get('imei')
    device = Device.query.filter_by(imei = imei).first_or_404()

    try:
        momsn = request.form.get('momsn')
        sender_id = 1 # TODO: lookup sender_id
        transmit_time = request.form.get('transmit_time')
        time = datetime.strftime(datetime.utcnow(), dt_fmt)
        iridium_latitude = request.form.get('iridium_latitude')
        iridium_longitude = request.form.get('iridium_longitude')
        iridium_cep = request.form.get('iridium_cep')
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8")
        msg = Message(
            device_id=device.id,
            sender_id=sender_id,
            message=text,
            momsn=momsn,
            transmit_time=transmit_time,
            time=time,
            iridium_latitude=iridium_latitude,
            iridium_longitude=iridium_longitude,
            iridium_cep=iridium_cep
        )
    except (ValueError, TypeError) as e:
        print('receive(): bad request: error processing parameters: {}'.format(e))
        return 'bad request: error processing parameters: {}'.format(e), 400

    # Add message to database
    try:
        db.session.add(msg)
        db.session.commit()
    except Exception as e:
        print('receive(): unable to add to database {}'.format(e))
        return 'unable to add to database {}'.format(e), 400

    return "done"
