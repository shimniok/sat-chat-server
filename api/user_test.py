from test_fixture import client, application
from user import endpoint

new_user = {
    'email': 'test@example.com',
    'name': 'Test',
    'password': 'Password'
}


def test_user_list(client):
    """Start with fresh database with initial user."""

    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)

    # only one user returned
    d = r.json #json.loads(r.data.decode())
    assert len(d) == 1
    u = d[0]

    # email field
    assert "email" in u, "email keyword missing"
    assert u['email'] == 'admin@example.com', "email doesn't match"
    assert "name" in u, "name keyword missing"
    assert u['name'] == 'admin', "name doesn't match"

    # Password not returned via api
    assert "password" not in u, "password is being returned by api"


def test_user_post(client):
    r = client.post(endpoint, json=new_user, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
    u = r.json
    assert 'id' in u
    r = client.get('/api/user/{}'.format(u['id']))
    assert r.status_code == 200, 'Error {}'.format(r.data)
    assert r.content_type == 'application/json'
    u = r.json
    assert u['name'] == new_user['name']
    assert u['email'] == new_user['email']


def test_user_delete(client):
    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200
    assert r.content_type == 'application/json'
    users = r.json
    for u in users:
         if u['email'] == new_user['email']:
             user = u
             break
    r = client.delete(endpoint+'/{}'.format(u['id']), content_type="application/json")
    assert r.status_code == 200
    assert r.content_type == "application/json"
    u = r.json
    assert u['email'] == new_user['email']
    assert u['name'] == new_user['name']
