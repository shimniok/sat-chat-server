from test_fixture import *
from models import *

def test_db_user(application):
    ''' User table should only contain 'admin' user '''
    users = User.query.all()
    assert len(users) == 1
    admin = User.query.filter_by(name='admin').first()
    assert admin != None, 'no admin user found'


def test_db_message(application):
    ''' Message table should be empty '''
    messages = Message.query.all()
    assert len(messages) == 0, 'table not empty'

def test_db_device(application):
    ''' Device table should be empty '''
    devices = Device.query.all()
    assert len(devices) == 0, 'table not empty'
