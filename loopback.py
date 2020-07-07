## LOOPBACK INTERFACE
# Simulates RockBLOCK web service for sending to mobile. The endpoint then echoes back
# a simulated reply from mobile, sent to the receive interface

import os
import binascii
import requests
from flask import Blueprint, request
from flask_login import current_user
from datetime import datetime, timezone

loopback = Blueprint('loopback', __name__)

# Loopback for testing only. Emulates Rock7 MT web service
@loopback.route('/loopback', methods=['post'])
def loopback_post():

    # Read static momsn message serial number
    try:
        momsn_file = "momsn.txt"
        with open(momsn_file, "r") as f:
            momsn_str = f.read()
            f.close()
    except OSError as e:
        return "FAILED,{}: error opening for read. {}".format(momsn_file, e),400

    # If we can't convert it to int, set it to 99
    try:
        momsn = int(momsn_str)
    except:
        momsn = 99

    ## Receive
    username = request.form.get('username')
    password = request.form.get('password')

    #TODO implement authentication
    #    if (username == app.config['USERNAME'] and password == app.config['PASSWORD']):

    imei = request.form.get('imei')
    #TODO validate imei

    # convert hex message back to text and add some text
    hex = request.form.get('data')
    text = binascii.a2b_hex(hex).decode("utf-8") + " reply"
    hex = binascii.b2a_hex(text.encode('utf-8'))

    mobile_momsn = momsn + 1 # the loopback simulates an MO message, incrementing the momsn again

    receive_url = os.environ['RECEIVE_ENDPOINT']
    message = {
        'imei': os.environ['IMEI'],
        'momsn': mobile_momsn,
        'transmit_time': datetime.strftime(datetime.now(timezone.utc), "%y-%m-%d %H:%M:%S"),
        'iridium_latitude': "39.5807",
        'iridium_longitude': "-104.8772",
        'iridium_cep': 8,
        'data': hex
    }
    r = requests.post(url=receive_url, data=message)

    # Update static momsn message serial number
    try:
        with open(momsn_file, "w") as f:
            f.write("{}\n".format(mobile_momsn + 1))
            f.close()
    except OSError as e:
        return "FAILED,{}: error opening for write. {}".format(momsn_file, e),400

    return "OK,{}".format(momsn)