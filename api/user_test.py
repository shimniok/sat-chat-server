from test_fixture import application, client, user1, shared_data
from user import endpoint, filter_phone, get_user_by_id

new_user = {
    'email': 'test@example.com',
    'name': 'Test',
    'password': 'Password',
    'phone': '555-555-5555',
    'admin': False
}


def test_user_list(client):
    """Start with fresh database with initial user."""

    r = client.get(endpoint, content_type="application/json")
    assert r.status_code == 200, 'Error {}'.format(r.data)

    # only one user returned
    u = r.json
    assert "email" in u, "email keyword missing"
    assert u['email'] == 'admin@example.com', "email doesn't match"
    assert "name" in u, "name keyword missing"
    assert u['name'] == 'admin', "name doesn't match"
    assert "phone" in u, "phone keyword missing"

    # Password not returned via api
    assert "password" not in u, "password is being returned by api"


def test_user_post_delete(client):
    # Post
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
    assert u['phone'] == new_user['phone']
    assert u['admin'] == new_user['admin']

    # Delete
    r = client.delete(
        endpoint+'/{}'.format(u['id']), content_type="application/json")
    assert r.status_code == 200
    assert r.content_type == "application/json"
    u = r.json
    assert u['name'] == new_user['name']
    assert u['email'] == new_user['email']
    assert u['phone'] == new_user['phone']
    assert u['admin'] == new_user['admin']
    r = client.get(endpoint+'/{}'.format(u['id']), content_type="application/json")
    assert r.status_code == 404
    
    
def test_filter_phone(client):
    assert filter_phone("+1-555-555-5555") == ""
    assert filter_phone("55-555-5555") == ""
    assert filter_phone("555-55-5555") == ""
    assert filter_phone("555-555-555") == ""
    assert filter_phone("555-555-5a55") == ""
    assert filter_phone("5555555555") == ""
    assert filter_phone("5555-555-5555") == ""
    assert filter_phone("555-5555-5555") == ""
    assert filter_phone("555-555-55555") == ""


def test_user_patch(user1):
    data1 = {
        'phone': '555-555-5000'
    }
    r1 = user1.patch(endpoint, json=data1, content_type="application/json")
    assert r1.status_code == 200, 'Error {}'.format(r.data)
    u1 = r1.json
    assert u1['phone'] == data1['phone']
    assert u1['phone'] != shared_data['user1']['phone']

    r2 = user1.get(endpoint+'/{}'.format(u1['id']), content_type="application/json")
    assert r2.status_code == 200, 'Error {}'.format(r2.data)
    u2 = r2.json
    assert u2['phone'] == u1['phone']
    assert u2['phone'] != shared_data['user1']['phone']
    

def test_get_user_by_id(user1):
    user = get_user_by_id(shared_data['user1_id'])
    assert user != None
    assert user.id == shared_data['user1_id']

