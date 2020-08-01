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

    m = Message(
        imei='abcdefg',
        sender_id=1,
        momsn=99,
        message='testing',
        transmit_time="2020-08-01T08:33Z",
        time="2021-09-02T11:22Z",
        iridium_latitude=-104.1234,
        iridium_longitude=39.4321,
        iridium_cep=4
    )
    #TODO: test variants of Message init
    assert m.imei == 'abcdefg'

def test_db_device(application):
    ''' Device table should be empty '''
    devices = Device.query.all()
    assert len(devices) == 0, 'table not empty'
