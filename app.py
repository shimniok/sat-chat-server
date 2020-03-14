import os
from flask import Flask, render_template, request
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

    print(hex)

    data = {'username': app.config['USERNAME'],
        'password': app.config['PASSWORD'],
        'imei': app.config['IMEI'],
        'data': hex
    }

    r = requests.post(url = app.config['API_ENDPOINT'], data = data )

    return render_template("send.html", r=r.text)


if __name__ == '__main__':
    app.run()
