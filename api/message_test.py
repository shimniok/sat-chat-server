import pytest
from test_fixture import application, client, user1, shared_data
from datetime import datetime, timezone
import binascii
from models import Message, db
from message import endpoint, get_latest_mt_message, get_latest_mo_message

# msg = {
#     'imei': shared_data['device1']['imei'],
#     'momsn': 999,
#     'transmit_time': "2020-07-25T06:12:30Z",
#     'time': "2020-07-25T06:13:45Z",
#     'iridium_latitude': 39.5807,
#     'iridium_longitude': -104.8772,
#     'iridium_cep': 8,
#     'message': 'my data' #binascii.b2a_hex('Test message'.encode('utf-8'))
# }


@pytest.fixture(scope="module")
def messages(user1):
    from api.device import get_my_device
    dev = get_my_device()

    from api.user import get_me
    me = get_me()

    from api.models import Message

    # create outgoing message #1
    msg1 = Message(
        device_id=dev.id,
        sender_id=me.id,
        message='outbound1',
        transmit_time="21-06-07 15:28:15",
        time="21-06-07 15:28:15"
    )
    db.session.add(msg1)

    # create outgoing message #2
    msg2 = Message(
        device_id=dev.id,
        sender_id=me.id,
        message='outbound2',
        transmit_time="21-06-07 15:35:45",
        time="21-06-07 15:35:45"
    )
    db.session.add(msg2)

    # create received message
    msg3 = Message(
        device_id=dev.id,
        message='inbound1',
        transmit_time="21-06-07 15:33:25",
        time="21-06-07 15:33:25"
    )
    db.session.add(msg3)

    # create received message
    msg4 = Message(
        device_id=dev.id,
        message='inbound2',
        transmit_time="21-06-07 15:37:41",
        time="21-06-07 15:37:41"
    )
    db.session.add(msg4)
    
    db.session.commit()

    yield [ msg1, msg2, msg3, msg4 ]

    db.session.delete(msg1)
    db.session.delete(msg2)
    db.session.delete(msg3)
    db.session.commit()


def test_empty_messages(client):
    # Make sure database is empty
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    messages = r.json
    assert len(messages) == 0, 'message list not 0 length'


def test_get_latest_mt(messages):
    m = get_latest_mt_message()
    assert m.message == messages[1].message

def test_get_latest_mo(messages):
    m = get_latest_mo_message()
    assert m.message == messages[3].message
    
    
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
