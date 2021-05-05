import pytest
import os
import json
from config import create_config
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from app import create_app
import api.models
import api.user
import api.device
from api.models import init_db as init_db

tmpdb_file = "/tmp/test.db"
tmpdb_uri = "sqlite:///{}".format(tmpdb_file)

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

    # Prepare environment
    test_config = create_config(env="Testing")
    test_config.SQLALCHEMY_DATABASE_URI = tmpdb_uri
    
    app = create_app(test_config)
    app.app_context().push()
    
    assert os.path.exists(tmpdb_file)

    yield app

#    if os.path.exists(tmpdb_file):
#        os.remove(tmpdb_file)


@pytest.fixture(scope='module')
def client(application):

    with application.test_client() as client:
        # Login
        r = client.post(api.auth.endpoint, json=admin_data, content_type='application/json')
        assert r.status_code == 200, 'Error: {}'.format(r.data)

        yield client


@pytest.fixture(scope='module')
def user1(client):
    
    # Create user1
    r = client.post(api.user.endpoint, json=user1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    user1_record = r.json

    # Create user2
    r = client.post(api.user.endpoint, json=user2_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    user2_record = r.json

    # log out of admin

    # log in as user1
    r = client.post(api.auth.endpoint, json=user1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    # Create device1 owned by user1
    r = client.post(api.device.endpoint, json=device1_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    device1_record = r.json
    assert device1_record['owner_id'] == user1_record['id']

    yield client

    r = client.post(api.auth.endpoint, json=admin_data, content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    r = client.delete(api.user.endpoint+'/{}'.format(user1_record['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    r = client.delete(
        api.user.endpoint+'/{}'.format(user2_record['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    r = client.delete(
        api.device.endpoint+'/{}'.format(device1_record['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
