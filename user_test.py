from test_fixture import *

def test_user_list(client):
    """Start with fresh database with initial user."""

    r = client.get('/api/user')
    assert r.status_code == 200

    # only one user returned
    d = json.loads(r.data.decode())
    assert len(d) == 1
    u = d[0]

    # email field
    assert "email" in u
    assert u['email'] == 'admin'
    assert u['name'] == 'admin'

    # Password not returned via api
    assert "password" not in u
