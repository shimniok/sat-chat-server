from app import db
from sqlalchemy.dialects.postgresql import JSON
import json

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    transmit_time = db.Column(db.String())
    time = db.Column(db.DateTime())

    #from_user = db.Column(db.String())
    #to_user = db.Column(db.String())
    #momsn = request.form.get('momsn')
    #iridium_latitude = request.form.get('iridium_latitude')
    #iridium_longitude = request.form.get('iridium_longitude')
    #iridium_cep = request.form.get('iridium_cep')
    #text = request.form.get('data')

    def __init__(self, message, transmit_time):
        self.message = message
        self.time = transmit_time

    def __repr__(self):
        return "Message(<id='{}', message='{}', transmit_time='{}'>)".format(
            self.id, self.message, self.time)


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
