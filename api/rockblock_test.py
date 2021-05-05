from test_fixture import user1, client, application, device1_data
from datetime import datetime
import binascii
from json_parser import dt_fmt
from api.message import endpoint as msg_endpoint
from api.rockblock import send_endpoint, receive_endpoint

text = 'Test Message'
mo_msg = {
    'imei': device1_data['imei'],
    'momsn': 99,
    'transmit_time': datetime.strftime(datetime.utcnow(), dt_fmt),
    'iridium_latitude': 39.5807,
    'iridium_longitude': -104.8772,
    'iridium_cep': 8.2,
    'data': binascii.b2a_hex(text.encode('utf-8'))
}

def test_rockblock_receive(user1):
    ''' Test the receive api '''
    # Send Mobile Originated simulated message;
    # Ensure receive API returns 'done' -- ok status
    r = user1.post(receive_endpoint, data=mo_msg)
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.data == b'done'

    # Ensure new message exist via message api
    r = user1.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 1
    m = r.json[0]

    # Verify the message matches the one posted to the api
    #assert m['imei'] == mo_msg['imei']
    assert m['momsn'] == mo_msg['momsn']
    assert m['transmit_time'] == mo_msg['transmit_time']
    assert m['iridium_latitude'] == mo_msg['iridium_latitude']
    assert m['iridium_longitude'] == mo_msg['iridium_longitude']
    assert m['iridium_cep'] == mo_msg['iridium_cep']
    assert m['message'] == text

    # Delete the message and make sure it's deleted
    r = user1.delete(
        msg_endpoint + '/{}'.format(m['id']), content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    r = user1.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 0

mt_msg = {
    "message": "This is a test"
}

def test_rockblock_send(user1):
    ''' Test the send api '''

    # Send the Mobile Terminated message
    r = user1.post(send_endpoint, json=mt_msg, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
    r = user1.get(msg_endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert len(r.json) == 1, 'unexpected json result length: {}'.format(r.json)
    m = r.json[0]

    # Ensure the message text matches the one we sent
    assert m['message'] == mt_msg['message']

    # Delete the message
    r = user1.delete(
        msg_endpoint+'/{}'.format(m['id']), content_type='application/json')
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
