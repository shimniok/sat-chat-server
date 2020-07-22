import pytest
from app import create_app
from models import db


@pytest.fixture(scope='session')
def app():
    '''
    Create a Flask app context for the tests.
    '''
    app = create_app()
    app.app_context().push()

    yield app


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
