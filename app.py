import os
import config
import requests
import binascii
from datetime import datetime
from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

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
@app.route('/api/send', methods=['POST'])
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
    list = []
    msg_bits = r.text.split(',')
    if msg_bits[0] == 'OK':
        result = {
            'status': msg_bits[0],
            'momsn': msg_bits[1]
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
    list.append(result)

    # TODO: store sent messages in database

    return jsonify(list)

# Receive data from Rock7
@app.route('/api/receive', methods=['POST'])
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

@app.route('/api/message', methods=['GET'])
def messages():
    list = []
    my_query = Message.query.order_by(Message.momsn).all()
    print(my_query)
#    db.session.query(
#        Message.id,
#        Message.momsn,
#        Message.message,
#        Message.iridium_latitude,
#        Message.iridium_longitude,
#        Message.iridium_cep)
    for m in my_query:
    #for i, momsn, m, dt, lat, lon, cep in my_query:
        list.append({
            'id': m.id,
            'momsn': m.momsn,
            'message': m.message,
            'time': m.transmit_time,
            'iridium_latitude': m.iridium_latitude,
            'iridium_longitude': m.iridium_longitude,
            'iridium_cep': m.iridium_cep
            })
    return jsonify(list)
    #print(">>> ", list)
    #return "ok" #message_list

@app.route('/api/message/<msg_id>', methods=['GET', 'DELETE'])
def message(msg_id=-1):
    if request.method == 'GET':
        my_query = Message.query().filter_by(momsn = msg_id).first()
        return jsonify(my_query)
        #"GET: The message id is %s" % (msg_id)

    if request.method == 'DELETE':
        return "DELETE: The message id is %s" % (msg_id)


if __name__ == '__main__':
    app.run()
