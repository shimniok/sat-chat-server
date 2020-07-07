## SEND/RECEIVE API ########################################################################################

import requests
import binascii
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from datetime import datetime, timezone
from .models import Message, db

rockblock = Blueprint('rockblock', __name__, url_prefix='/api', template_folder='templates')

@rockblock.before_request
def rockblock_before():
    if not current_user.is_authenticated:
        return "Unauthorized", 401


# Send data to Rock7
@rockblock.route('/send', methods=['post'])
def send():

    text = request.form.get('message')
    hex = binascii.b2a_hex(text.encode('utf-8'))
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
    if msg_bits[0] == 'OK':
        #TODO: add IMEI column, to/from
        m = Message(
            momsn=msg_bits[1],
            message=text,
            transmit_time=datetime.strftime(datetime.now(timezone.utc), "%y-%m-%d %H:%M:%S")
        )
        id = db.session.add(m)
        db.session.commit()
        result = {
            'status': msg_bits[0],
            'message': m.to_dict()
        }
    elif msg_bits[0] == 'FAILED':
        result = {
            'status': msg_bits[0],
            'error_number': msg_bits[1],
            'error_text': msg_bits[2]
        }
    else:
        result = {
            'status': "FAILED",
            'error_number': "999",
            'error_text': r.text
        }

    return jsonify(result)


# Receive data from Rock7
@rockblock.route('/receive', methods=['post'])
def receive():

    imei = request.form.get('imei')
    if (imei == rockblock.config['IMEI']):
        momsn = request.form.get('momsn')
        transmit_time = datetime.strptime(request.form.get('transmit_time'), "%y-%m-%d %H:%M:%S")
        iridium_latitude = request.form.get('iridium_latitude')
        iridium_longitude = request.form.get('iridium_longitude')
        iridium_cep = request.form.get('iridium_cep')
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8")

        # Add message to database
        try:
            msg = Message(
                message=text, momsn=momsn, transmit_time=transmit_time,
                iridium_latitude=iridium_latitude, iridium_longitude=iridium_longitude,
                iridium_cep=iridium_cep)
            db.session.add(msg)
            db.session.commit()
        except:
            return 'unable to add to database', 400
    else:
        return 'imei mismatch', 400

    return "done"
