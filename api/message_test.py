from test_fixture import *
from datetime import datetime, timezone
import binascii
from models import Message
from message import endpoint

msg = {
    'imei': device1_data['imei'],
    'momsn': 999,
    'transmit_time': "2020-07-25T06:12:30Z",
    'time': "2020-07-25T06:13:45Z",
    'iridium_latitude': 39.5807,
    'iridium_longitude': -104.8772,
    'iridium_cep': 8,
    'message': 'my data' #binascii.b2a_hex('Test message'.encode('utf-8'))
}


def test_empty_messages(client):
    # Make sure database is empty
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    messages = r.json
    assert len(messages) == 0, 'message list not 0 length'

# TODO: Test message get

# TODO: Test message get?since_id

# TODO: Test message post

# TODO: Test message delete

'''
def test_post_messages(client):
    # Post new message_get
    r = client.post(endpoint, json=msg, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    m = r.json

    #TODO: assert m['imei'] == new['imei']
    assert m['momsn'] == msg['momsn']
    assert m['transmit_time'] == msg['transmit_time']
    assert m['time'] == msg['time']
    assert m['iridium_latitude'] == msg['iridium_latitude']
    assert m['iridium_longitude'] == msg['iridium_longitude']
    assert m['message'] == msg['message']

def test_delete_messages(client):
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(list) == 1
    list = r.json
    for m in list:
        client.delete('{}/{}'.format(endpoint, m['id']), content_type="application/json")
        assert r.status_code == 200, 'Error {}'.format(r.data)
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    list = r.json
    assert len(list) == 0
'''
