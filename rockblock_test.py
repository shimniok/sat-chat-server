from test_fixture import *

send_data = {
    "message": "This is a test"
}

def test_send(client):
    r = client.post('/api/send', json=send_data, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
