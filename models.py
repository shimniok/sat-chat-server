from app import db
from sqlalchemy.dialects.postgresql import JSON
import json
from output_mixin import OutputMixin

class Message(OutputMixin, db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    momsn = db.Column(db.Integer)
    message = db.Column(db.String())
    transmit_time = db.Column(db.String())
    time = db.Column(db.DateTime())
    iridium_latitude = db.Column(db.Float())
    iridium_longitude = db.Column(db.Float())
    iridium_cep = db.Column(db.Integer)

    def __repr__(self):
        return "Message(<id='{}', momsn='{}' message='{}', transmit_time='{}', iridium_latitude='{}', iridium_longitude='{}', iridium_cep='{}'>)".format(
            self.id, self.momsn, self.message, self.time, self.iridium_latitude, self.iridium_longitude, self.iridium_cep)

#class User(db.Model):
#    __tablename__ = 'users'
#
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String)
#    password = db.Column(db.String)
#    email = db.Column(db.String)
#
#    def __init__(self, username, password, email):
#        self.username = username
#        self.password = password
#        self.email = email
#
#    def __repr__(self):
#        return '<id {}>'.format(self.id)
