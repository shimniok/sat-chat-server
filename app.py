import os
from flask import Flask, render_template, request
import config
import requests

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/api/send', methods=['post'])
def send():
    text = request.form.get('message')

    data = {'username': app.config['USERNAME'],
        'password': app.config['PASSWORD'],
        'imei': app.config['IMEI'],
        'data': text.encode('hex')
    }

    r = requests.post(url = API_ENDPOINT, data = data)

    return r


if __name__ == '__main__':
    app.run()
