import pytest
from test_fixture import *

def test_loopback(client):
    # Send
    data = { "message": "testing" }
#    r = client.post("/loopback", data=data, content_type="application/text")
#    assert r.status_code == 200
