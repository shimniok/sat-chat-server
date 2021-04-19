import pytest
import os
from app import create_app
from models import db, User, init_db
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
import json
import user
import device

tmpdb_file = "/tmp/test.db"
tmpdb_uri = 'sqlite:///{}'.format(tmpdb_file)

admin_data = {
    "email": "admin@example.com",
    "password": "admin",
    "remember": 1
}

user1_data = {
    'email': "user1@example.com",
    'name': 'User1',
    'password': 'user1',
    'remember': 1
}

user2_data = {
    'email': "user2@example.com",
    'name': 'User2',
    'password': 'user2',
    'remember': 1
}

device1_data = {
    'imei': '300234010753370',
    'username': 'device1@example.com',
    'password': 'device1'
}


@pytest.fixture(scope='module')
def application():
    '''
    Create a Flask app context for the tests.
    '''

    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = tmpdb_uri
    app.app_context().push()
    init_db(app)

    yield app


@pytest.fixture(scope='module')
def client(application):

    with application.test_client() as client:
        # Login
        r = client.post('/auth', json=admin_data, content_type='application/json')
        assert r.status_code == 200,'unable to login as admin user'

        yield client


@pytest.fixture(scope='module')
def user1(client):

    # Create user1
    r = client.post(user.endpoint, json=user1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    user1 = r.json
    user1_data['id'] = r.json['id']

    # Create user2
    r = client.post(user.endpoint, json=user2_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    user2 = r.json
    user2_data['id'] = r.json['id']

    # log out of admin
    #r = client.get('/auth', content_type='application/json')
    #assert r.status_code == 200, 'Error: {}'.format(r.data)
    #me = r.json
    #assert me['id'] == 1
    #r = client.delete('/auth/{}'.format(me['id']), content_type='application/json')

    # log in as user1
    r = client.post('/auth', json=user1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    # Create device1 owned by user1
    r = client.post(device.endpoint, json=device1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    device1 = r.json
    device1_data['id'] = r.json['id']

    yield client

    r = client.post('/auth', json=admin_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    r = client.delete(user.endpoint+'/{}'.format(user1['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    r = client.delete(user.endpoint+'/{}'.format(user2['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    r = client.delete(device.endpoint+'/{}'.format(device1['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
