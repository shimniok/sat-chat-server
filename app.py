from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import config
import requests
import binascii

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Message


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

    #TODO parse return from request and return json

    return render_template("send.html", r=r.text)

# Receive data from Rock7
@app.route('/api/receive', methods=['post'])
def receive():
    imei = request.form.get('imei')
    if (imei == app.config['IMEI']):
        momsn = request.form.get('momsn')
        transmit_time = request.form.get('transmit_time')
        iridium_latitude = request.form.get('iridium_latitude')
        iridium_longitude = request.form.get('iridium_longitude')
        iridium_cep = request.form.get('iridium_cep')
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8")

        #try:
        #    result = Message(message=text)
        #    db.session.add(result)
        #    db.session.commit()
        #except:
        #    errors.append("Unable to add item to database.")

        #TODO parse return from request and return json

        return "done"


if __name__ == '__main__':
    app.run()
