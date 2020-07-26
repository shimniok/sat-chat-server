from test_fixture import *
from models import User, Message, db

def test_db_user(application):
    # User table should only contain 'admin' user
    users = User.query.all()
    assert len(users) == 1
    admin = User.query.filter_by(name='admin').first()
    assert admin != None


def test_db_message(application):
    # Empty table
    messages = Message.query.all()
    assert len(messages) == 0, 'table not empty'
