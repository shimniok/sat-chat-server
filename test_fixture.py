import pytest
import os
from app import create_app
from models import db, User, init_db
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

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

    #print('Removing temporary database')
    #os.unlink(tmpdb_file)


@pytest.fixture(scope='module')
def client(application):

#    alembic_config = AlembicConfig("./migrations/alembic.ini")
#    alembic_config.set_main_option("script_location", "./migrations")
#    alembic_config.set_main_option('sqlalchemy.url', tmpdb_uri)
#    alembic_upgrade(alembic_config, 'head')
#op.bulk_insert(accounts_table, [
#{'username': 'admin', 'email': '', 'password': 'sha256$Gvk5fRPF$74462c8a5da334bf551b2943eda4604ba4ae4ba3ec7f0d86154238ef7aaa8e3d'}
#])

    with application.test_client() as client:
        yield client

    #os.unlink(tmpdb_file)


#@pytest.fixture(scope='session')
#def database(app):
#
#    return database


#@pytest.fixture(scope='session')
#def _db(app):
#    '''
#    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
#    database connection.
#    '''
#    return db.session

#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#    db = SQLAlchemy(app=app)
#    db.create_all()
#
#    return db
