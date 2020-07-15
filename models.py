from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import json
from output_mixin import OutputMixin
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

#TODO: create roles table, add role Column to each user
#TODO: add Devices, assign device to user as owner / sender

class Message(OutputMixin, db.Model):
    __tablename__ = 'messages'
    RELATIONSHIPS_TO_DICT = True

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sender = db.relationship("User")
    momsn = db.Column(db.Integer)
    message = db.Column(db.String())
    transmit_time = db.Column(db.DateTime())
    time = db.Column(db.DateTime())
    iridium_latitude = db.Column(db.Float())
    iridium_longitude = db.Column(db.Float())
    iridium_cep = db.Column(db.Integer)

    def __repr__(self):
        return "Message(<id='{}', momsn='{}' message='{}', transmit_time='{}', iridium_latitude='{}', iridium_longitude='{}', iridium_cep='{}'>)".format(
            self.id, self.momsn, self.message, strftime(self.transmit_time, '%y-%m-%d %H:%M:%S'),
            strftime(self.time, '%y-%m-%d %H:%M:%S'), self.iridium_latitude, self.iridium_longitude,
            self.iridium_cep)

class User(OutputMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    PROTECTED_COLUMNS = [ 'password' ]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    device = db.relationship('Device', uselist=False, back_populates='owner')

    def __repr__(self):
        return "User(<id='{}', name='{}', email='{}'>".format(
            self.id, self.name, self.email)

class Device(OutputMixin, db.Model):
    __tablename__ = 'devices'
    PROTECTED_COLUMNS = [ 'IMEI', 'password' ]

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', back_populates='device')
    imei = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, owner_id, imei, username, password):
        self.owner_id = owner_id
        self.imei = imei
        self.username = username
        self.password = password

    def __repr__(self):
        return "Device(<id='{}', owner='{}', imei='{}', username='{}'".format(
            self.id, self.owner.email, self.imei, self.username )

class Connection(OutputMixin, db.Model):
    __tablename__ = 'connections'
    PROTECTED_COLUMNS = [ ]

    id = db.Column(db.Integer, primary_key=True)
    #device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    #device = db.relationship("Device", uselist=False, back_populates='devices')
    #connected_user_id = 0

    def __repr__(self):
        return ""
