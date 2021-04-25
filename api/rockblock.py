## SEND/RECEIVE API ########################################################################################

import requests
import binascii
import json
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from datetime import datetime, timezone
from json_parser import dt_fmt
from api.device import get_my_device, get_device_by_imei
from api.models import Message, Device, User, db

send_endpoint = "/api/send"
receive_endpoint = "/api/receive"

rockblock_bp = Blueprint('rockblock', __name__, template_folder='templates')

# TODO: Convert to using message api versus databse

# Send data to Rock7


@rockblock_bp.route(send_endpoint, methods=['post'])
def send():
    print("rockblock.send()")

    if not current_user.is_authenticated:
        return "Unauthorized", 401

    # Get my device
    my_device = get_my_device()
    if my_device == None:
        print("device not found")
        return "device not found", 404

    #################################################################
    ## Prepare message for sending to Rock7 endpoint
    ##
    try:
        #TODO: data = request.json
        data = json.loads(request.data.decode())
        text = data["message"]
        
        if text == "" or text == None:
            return "bad request: empty message", 400

        hex = binascii.b2a_hex(text.encode('utf-8'))
        print("send() text={} hex={}".format(text, hex))
    except Exception as e:
        print("send(): problem preparing message {}".format(e))
        return "error preparing message", 400

    data = {
        'username': my_device.username,
        'password': my_device.password,
        'imei': my_device.imei,
        'data': hex
    }
    r = requests.post(url = current_app.config['API_ENDPOINT'], data = data)

    print("send(): message posted, status={} {}".format(r.status_code, r.text))

    #################################################################
    ## Parse return from request and return json
    ##   Success: OK,12345678  --The number uniquely identifies your message.
    ##   Failure: FAILED,15,Textual description of failure
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
            device_id=my_device.id,
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
        print("{}".format(result['error_text']))
    return jsonify(result)


## receive
## Receive data from Rock7
## 
@rockblock_bp.route(receive_endpoint, methods=['get','post'])
def receive():

    print("rockblock.receive()")

    parameters = [
        'imei', 'momsn', 'transmit_time', 'iridium_latitude', 
        'iridium_longitude', 'iridium_cep', 'data'
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

    # match IMEI to a device
    device = get_device_by_imei( request.form.get('imei') )
    try:
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8")
        msg = Message(
            device_id=device.id,
            message=text,
            momsn=request.form.get('momsn'),
            transmit_time=request.form.get('transmit_time'),
            time=datetime.strftime(datetime.utcnow(), dt_fmt),
            iridium_latitude=request.form.get('iridium_latitude'),
            iridium_longitude=request.form.get('iridium_longitude'),
            iridium_cep=request.form.get('iridium_cep')
        )
        # Add message to database
        db.session.add(msg)
        db.session.commit()
    except (ValueError, TypeError) as e:
        print('receive(): bad request: error processing parameters: {}'.format(e))
        return 'bad request: error processing parameters: {}'.format(e), 400
    except Exception as e:
        print('receive(): unable to add to database {}'.format(e))
        return 'unable to add to database {}'.format(e), 400

    return "done"
