from test_fixture import *
from models import User, Message, db

def test_db_user(application):
    # User table should only contain 'admin' user
    users = User.query.all()
    assert len(users) == 1
    admin = User.query.filter_by(name='admin').first()
    assert admin != None

    # Add a user
    u = User()
    u.name = "Testing"
    u.email = "test@example.com"
    u.password = "asdf1234"
    db.session.add(u)
    db.session.commit()
    new = User.query.filter_by(name = u.name).first()
    assert new != None
    assert new.name == u.name
    assert new.email == u.email
    assert new.password == u.password
    assert new.id == 2

    # Delete user
    db.session.delete(new)
    db.session.commit()
    new = User.query.filter_by(name = u.name).first()
    assert new == None
    users = User.query.all()
    assert len(users) == 1
    admin = User.query.filter_by(name='admin').first()
    assert admin != None


def test_db_message(application):
    # Empty table
    messages = Message.query.all()
    assert len(messages) == 0, 'table not empty'

    # Add a message
    m = Message()
    m.message = "test message"
    m.iridium_latitude = 12.3456
    m.iridium_longitude = 65.4321
    m.iridium_cep = 8
    db.session.add(m)
    messages = Message.query.all()
    assert len(messages) == 1, 'should be 1 row in table'

    # Delete message
    db.session.delete(m)
    messages = Message.query.all()
    assert len(messages) == 0, 'table not empty'
