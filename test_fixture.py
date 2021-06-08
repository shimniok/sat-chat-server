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

shared_data = {}

@pytest.fixture(scope='session')
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


@pytest.fixture(scope='module')
def client(application):

    with application.test_client() as my_client:
        
        shared_data['admin'] = {
            "email": "admin@example.com",
            "name": "admin",
            "password": "admin",
            "remember": 1
        }
        
        # Login
        r = my_client.post(
            api.auth.endpoint, json=shared_data['admin'], content_type='application/json')
        assert r.status_code == 200, 'Error: {}'.format(r.data)

        shared_data['user_count'] = 1
        
        yield my_client


@pytest.fixture(scope='module')
def user1(client):
    global user1_record
    global shared_data
    
    shared_data['user1'] = {
        'email': "user1@example.com",
        'name': 'User1',
        'password': 'user1',
        'phone': '303-555-5555' # fake test phone number
    }


    shared_data['device1'] = {
        'imei': '300234010753370',
        'username': 'device1@example.com',
        'password': 'device1'
    }
    
    # user2_data = {
    #     'email': "user2@example.com",
    #     'name': 'User2',
    #     'password': 'user2',
    #     'phone': '555-555-5552'
    # }

    # Create user1
    r = client.post(api.user.endpoint, json=shared_data['user1'], content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    user1_record = r.json
    shared_data['user1_id'] = user1_record['id']

    shared_data['user_count'] += 1
    
    # Create user2
    # r = client.post(api.user.endpoint, json=user2_data, content_type='application/json')
    # assert r.status_code == 200, 'Error: {}'.format(r.data)
    # user2_record = r.json

    # log out of admin

    # log in as user1
    r = client.post(api.auth.endpoint,
                    json=shared_data['user1'], content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    # Create device1 owned by user1
    r = client.post(api.device.endpoint,
                    json=shared_data['device1'], content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
    device1_record = r.json
    assert device1_record['owner_id'] == user1_record['id']

    yield client

    r = client.post(api.auth.endpoint,
                    json=shared_data['admin'], content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    r = client.delete(
        api.user.endpoint+'/{}'.format(user1_record['id']
                                       ), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)

    # r = client.delete(
    #     api.user.endpoint+'/{}'.format(user2_record['id']), content_type='application/json')
    # assert r.status_code == 200, 'Error: {}'.format(r.data)

    r = client.delete(
        api.device.endpoint+'/{}'.format(device1_record['id']), content_type='application/json')
    assert r.status_code == 200, 'Error: {}'.format(r.data)
