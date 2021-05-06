## LOOPBACK INTERFACE
# Simulates RockBLOCK web service for sending to mobile. The endpoint then echoes back
# a simulated reply from mobile, sent to the receive interface

import os
import binascii
import requests
from flask import Blueprint, request, url_for, current_app
from flask_login import current_user
from datetime import datetime, timezone
from worker import q
from api.device import get_my_device
from api.models import rock7_date_format

endpoint="/api/loopback"

loopback_bp = Blueprint('loopback', __name__)
momsn_file = "momsn.txt"

def do_send(url, message):
    r = requests.post(url=url, data=message)
    print("-- loopback: do_send: url={} message={} status={}".format(url, message, r.status_code))
    return


# Loopback for testing only. Emulates Rock7 MT web service
@loopback_bp.route(endpoint, methods=['post'])
def loopback_post():
    global momsn_file

    ## Receive
    imei = request.form.get('imei')
    username = request.form.get('username')
    password = request.form.get('password')

    app = current_app

    # TODO: Simulate authentication with IMEI, USERNAME, PASSWORD

    # convert hex message back to text and add some text
    try:
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8") + " reply"
        hex = binascii.b2a_hex(text.encode('utf-8'))
    except Exception as e:
        print("-- loopback: conversion error: {}".format(e))

    # Read static momsn message serial number
    momsn_str = ""
    try:
        with open(momsn_file, "r") as f:
            momsn_str = f.read()
            f.close()
    except OSError as e:
        print("-- loopback: momsn: {}: {}".format(momsn_file, e))

    try:
        momsn = int(momsn_str)
    except:
        momsn = 99

    mobile_momsn = momsn + 1 # the loopback simulates an MO message, incrementing the momsn again

    url = request.url_root + url_for('rockblock.receive')[1:]
    message = {
        'imei': imei,
        'momsn': mobile_momsn + 1,
        'transmit_time': datetime.strftime(datetime.utcnow(), rock7_date_format),
        'iridium_latitude': "39.5807",
        'iridium_longitude': "-104.8772",
        'iridium_cep': 8.7,
        'data': hex
    }
    #from loopback import do_send
    job = q.enqueue_call(
           func = do_send, args = (url,message,), result_ttl=5000
        )
    print("-- loopback: job id: {}".format(job.get_id()))

    # Update static momsn message serial number
    try:
        with open(momsn_file, "w") as f:
            f.write("{}\n".format(mobile_momsn + 1))
            f.close()
    except OSError as e:
        print("FAILED,{}: error opening for write. {}".format(momsn_file, e))

    return "OK,{}".format(mobile_momsn)
