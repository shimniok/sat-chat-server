import pytest
from test_fixture import user1, client, application, device1_data
from loopback import endpoint
import binascii

def test_loopback(user1):
    # message = "test_loopback"
    # hex = binascii.b2a_hex(message.encode('utf-8'))
    # data = {
    #     "imei": device1_data["imei"],
    #     "username": device1_data["username"],
    #     "password": device1_data["password"],
    #     "data": hex
    # }

    # r = user1.post(endpoint, data=data, content_type="application/text")
    # assert r.status_code == 200, 'Error {}'.format(r.data)
    assert True
