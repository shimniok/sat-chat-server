from test_fixture import app
from models import User, Message, db

def test_db_user(app):
    # Empty table
    users = User.query.all()
    assert len(users) == 0, 'table not empty'

    # Add a user
    u = User()
    u.name = "Testing"
    u.email = "test@example.com"
    u.password = "asdf1234"
    db.session.add(u)
    users = User.query.all()
    assert len(users) == 1, 'should be 1 row in table'

    # Delete user
    db.session.delete(u)
    users = User.query.all()
    assert len(users) == 0, 'table not empty'


def test_db_message(app):
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
