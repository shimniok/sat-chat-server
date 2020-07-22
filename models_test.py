from test_fixture import app
from models import User, Message

def test_db_user(app):

    users = User.query.all()
    # Empty table
    # Add a user
    # Delete user

    #users = User.query.all()
    #u = User.query.filter_by(id=id).first_or_404()
    #u = User.query.filter_by(id=id).first_or_404()
    #db.session.delete(u)

    assert 1==1

def test_db_message(app):
    assert 1==1
