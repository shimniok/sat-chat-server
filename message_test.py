from test_fixture import *
from datetime import datetime, timezone
import binascii
from models import Message

endpoint = '/api/message'

new = {
    #'imei': os.environ['IMEI'],
    'momsn': 999,
    'transmit_time': "20-07-25 06:12:30",
    'time': "20-07-25 06:12:30",
    'iridium_latitude': 39.5807,
    'iridium_longitude': -104.8772,
    'iridium_cep': 8,
    'message': 'my data' #binascii.b2a_hex('Test message'.encode('utf-8'))
}

def test_messages(client):
    # Make sure database is empty
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200
    messages = r.json
    assert len(messages) == 0

    # Post new message_get
    r = client.post(endpoint, json=new, content_type="application/json")
    assert r.status_code == 200
    #m = r.json
    #assert m['imei'] == new['imei']
    #assert m['momsn'] == new['momsn']
    #assert m['transmit_time'] == new['transmit_time']
    #assert m['iridium_latitude'] == new['iridium_latitude']
