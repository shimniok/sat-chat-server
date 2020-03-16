import os
from flask import Flask, render_template, request, url_for
import config
import requests
import binascii

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
    return render_template("index.html")


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


@app.route('/api/receive', methods=['post'])
def receive():
    imei = request.form.get('imei')
    if (imei == app.config['IMEI']):
        momsn = request.form.get('momsn')
        transmit_time = request.form.get('transmit_time')
        iridium_latitude = request.form.get('iridium_latitude')
        iridium_longitude = request.form.get('iridium_longitude')
        iridium_cep = request.form.get('iridium_cep')
        text = request.form.get('data')

        #TODO parse return from request and return json

        return "done"


if __name__ == '__main__':
    app.run()
