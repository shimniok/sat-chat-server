import pytest
from test_fixture import user1, client, application, shared_data
from datetime import datetime
import binascii
from api.message import endpoint as msg_endpoint
from api.rockblock import send_endpoint, receive_endpoint
from api.models import json_date_format, rock7_date_format, decode_date

text = 'Test Message'


@pytest.fixture(scope='module')
def rockblock(user1):
    shared_data['mo_msg'] = {
        'imei': shared_data['device1']['imei'],
        'momsn': 99,
        # date format: 12-10-10 10:41:50
        'transmit_time': datetime.strftime(datetime.utcnow(), rock7_date_format),
        'iridium_latitude': 39.5807,
        'iridium_longitude': -104.8772,
        'iridium_cep': 8.2,
        'data': binascii.b2a_hex(text.encode('utf-8'))
    }
    
    shared_data['mt_msg'] = {
        "message": "This is a test"
    }
    
    yield user1


def test_rockblock_receive(rockblock):
    ''' Test the receive api '''
    # Send simulated Mobile Originated message;
    # Ensure receive API returns 'done' -- ok status
    r = rockblock.post(receive_endpoint, data=shared_data['mo_msg'])
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.data == b'done'

    # Ensure new message exist via message api
    r = rockblock.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 1
    m = r.json[0]

    # Verify the message matches the one posted to the api
    #assert m['imei'] == shared_data['mo_msg']['imei']
    assert m['momsn'] == shared_data['mo_msg']['momsn']
    assert decode_date(m['transmit_time']) == decode_date(
        shared_data['mo_msg']['transmit_time'])
    assert m['iridium_latitude'] == shared_data['mo_msg']['iridium_latitude']
    assert m['iridium_longitude'] == shared_data['mo_msg']['iridium_longitude']
    assert m['iridium_cep'] == shared_data['mo_msg']['iridium_cep']
    assert m['message'] == text

    # Delete the message and make sure it's deleted
    r = rockblock.delete(
        msg_endpoint + '/{}'.format(m['id']), content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    r = rockblock.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 0


def test_rockblock_receive_empty(rockblock):
    ''' Test the receive api '''
    # Send Mobile Originated empty message;
    # Ensure receive API returns 'done' -- ok status -- and message ignored
    mo_msg2 = shared_data['mo_msg']
    mo_msg2['data'] = ""

    r = rockblock.post(receive_endpoint, data=mo_msg2)
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.data == b'done'

    # Ensure new message exist via message api
    r = rockblock.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 0, 'expected json result length: {}'.format(r.json[0])


def test_rockblock_send(rockblock):
    ''' Test the send api '''

    # Send the Mobile Terminated message
    r = rockblock.post(send_endpoint, json=shared_data['mt_msg'], content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
    r = rockblock.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 1, 'unexpected json result length: {}'.format(r.json)
    m = r.json[0]

    # Ensure the message text matches the one we sent
    assert m['message'] == shared_data['mt_msg']['message']

    # Delete the message
    r = rockblock.delete(
        msg_endpoint+'/{}'.format(m['id']), content_type='application/json')
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
