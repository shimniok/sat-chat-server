import pytest
import os
from app import create_app
from models import db, User, init_db
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
import json

tmpdb_file = "/tmp/test.db"
tmpdb_uri = 'sqlite:///{}'.format(tmpdb_file)


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
        data = {
            "email": "admin",
            "password": "admin",
            "remember": 1
        }
        r = client.post('/auth', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 200,'unable to login as admin user'

        yield client
