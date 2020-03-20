import os
import config
import requests
import binascii
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

    #TODO parse return from request and return json

    return render_template("send.html", r=r.text)

# Receive data from Rock7
@app.route('/api/receive', methods=['POST'])
def receive():
#    status_code = status.HTTP_400_BAD_REQUEST
#    error_msg = { 'error': 'generic error' }
    imei = request.form.get('imei')
    if (imei == app.config['IMEI']):
        momsn = request.form.get('momsn')
        transmit_time = request.form.get('transmit_time')
        iridium_latitude = request.form.get('iridium_latitude')
        iridium_longitude = request.form.get('iridium_longitude')
        iridium_cep = request.form.get('iridium_cep')
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8")

        # Add message to database
        try:
            msg = Message(message = text)
            db.session.add(msg)
            db.session.commit()
            status_code = status.HTTP_200_OK
        except:
            #TODO: secure error message & logging
            error_msg = { 'error': 'unable to add to database' }
    else:
        error_msg = { 'error': 'imei mismatch' }
        status_code = status.HTTP_400_BAD_REQUEST

    return "done"

@app.route('/api/message', methods=['GET'])
def messages():
    list = []
    for i, m in db.session.query(Message.id, Message.message):
        list.append({'id': i, 'message': m})
    return jsonify(list)
    #print(">>> ", list)
    #return "ok" #message_list


if __name__ == '__main__':
    app.run()
