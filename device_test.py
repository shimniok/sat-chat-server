from test_fixture import *
from flask import request
from models import Device

def test_device(client):
    """Start with fresh database."""

    r = client.get('/api/device', content_type="application/json")
    assert r.status_code == 200
    assert r.content_type == 'application/json'
    assert len(r.json) == 0

    new = Device(
        imei='abcdefg',
        username='bogus',
        password='alsobogus'
    )

    data = json.dumps(new.to_dict())

#    r = client.post('/api/device', data=data, content_type="application/json")
#    assert r.status_code == 200
#    assert r.content_type == 'application/json'

    # only one user returned
#    d = json.loads(r.data.decode())
#    assert len(d) == 1
#    u = d[0]

#    # email field
#    assert "email" in u
#    assert u['email'] == 'admin'
#    assert u['name'] == 'admin'

    # Password not returned via api
#    assert "password" not in u
