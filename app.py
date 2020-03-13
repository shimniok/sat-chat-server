import os
from flask import Flask
from flask import render_template
import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/api/send', methods=['post'])
def send():
    return "Send!"


if __name__ == '__main__':
    app.run()
