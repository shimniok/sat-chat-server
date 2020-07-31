from test_fixture import *
from flask import request
from models import Device
from device import endpoint

dev = {
    'imei': 'abcdefg',
    'username': 'bogus',
    'password': 'alsobogus'
}

def test_empty_devices(client):
    """Start with fresh database."""

    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
    assert r.json == {}

def test_post_device(client):

    r = client.post(endpoint, json=dev, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'

    r = client.get(endpoint, content_type="application/json")
    d = r.json
    assert d['imei'] == dev['imei']
    assert d['username'] == dev['username']

def test_delete_device(client):
    r = client.get(endpoint, content_type="application/json")
    d = r.json

    r = client.delete(endpoint+'/{}'.format(d['id']), content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'

    r = client.get(endpoint, content_type="application/json")
    assert r.json == {}
