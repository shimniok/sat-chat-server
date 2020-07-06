import os
import config
import requests
import binascii
from datetime import datetime
from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


#TODO implement authentication
#TODO log accesses


@app.route('/')
def hello():
    return render_template("index.html")

# Send data to Rock7
@app.route('/api/send', methods=['post'])
def send():
    text = request.form.get('message')
    hex = binascii.b2a_hex(text.encode('utf-8'))

    data = {
        'username': app.config['USERNAME'],
        'password': app.config['PASSWORD'],
        'imei': app.config['IMEI'],
        'data': hex
    }

    r = requests.post(url = app.config['API_ENDPOINT'], data = data )

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
            'error_text': "unrecognized status received"
        }

    return jsonify(result)

# Receive data from Rock7
@app.route('/api/receive', methods=['post'])
def receive():
    imei = request.form.get('imei')
    if (imei == app.config['IMEI']):
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


@app.route('/api/message', methods=['get'])
def messages():
    list = []
    msgs = Message.query.order_by(Message.momsn).all()
    return jsonify([m.to_dict() for m in msgs])


@app.route('/api/message/<msg_id>', methods=['get', 'delete'])
def message(msg_id=-1):
    msg = Message.query.filter_by(id = msg_id).first_or_404()

    if request.method == 'GET':
        return jsonify(msg.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        return jsonify(msg.to_dict())


# Loopback for testing only. Emulates Rock7 MT web service
@app.route('/api/loopback', methods=['get','post'])
def loopback():
    if app.config['LOOPBACK_ENABLED'] == False:
        return "FAILED",400

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

if __name__ == '__main__':
    app.run()
