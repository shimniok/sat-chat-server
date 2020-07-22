from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy, Model
#from sqlalchemy.dialects.postgresql import JSON
#import json
from output_mixin import OutputMixin
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

#TODO: create roles table, add role Column to each user
#TODO: add Devices, assign device to user as owner / sender


class Message(OutputMixin, db.Model):
    __tablename__ = 'messages'
    RELATIONSHIPS_TO_DICT = True

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship("User")
    momsn = Column(Integer)
    message = Column(String())
    transmit_time = Column(DateTime())
    time = Column(DateTime())
    iridium_latitude = Column(Float())
    iridium_longitude = Column(Float())
    iridium_cep = Column(Integer)

    def __repr__(self):
        return "Message(<id='{}', momsn='{}' message='{}', transmit_time='{}', iridium_latitude='{}', iridium_longitude='{}', iridium_cep='{}'>)".format(
            self.id, self.momsn, self.message, strftime(self.transmit_time, '%y-%m-%d %H:%M:%S'),
            strftime(self.time, '%y-%m-%d %H:%M:%S'), self.iridium_latitude, self.iridium_longitude,
            self.iridium_cep)

class User(OutputMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    PROTECTED_COLUMNS = [ 'password' ]

    id = Column(Integer, primary_key=True)
    email = Column(String(), unique=True)
    name = Column(String())
    password = Column(String())
    #device = relationship("Device", uselist=False, back_populates="owner")

    def __repr__(self):
        return "User(<id='{}', name='{}', email='{}'>".format(
            self.id, self.name, self.email)

class Device(OutputMixin, db.Model):
    __tablename__ = 'devices'
    PROTECTED_COLUMNS = [ 'IMEI', 'password' ]

    id = Column(Integer, primary_key=True)
    #owner_id = Column(Integer, ForeignKey("users.id"))
    #owner = relationship("User", back_populates="device")
    imei = Column(String())
    username = Column(String())
    password = Column(String())

    def __repr__(self):
        return "Device(<id='{}', imei='{}', username='{}'".format(
            self.id, self.imei, self.username )

#class Connection(OutputMixin, Model):
#    __tablename__ = 'connections'
#    PROTECTED_COLUMNS = [ ]

#    id = Column(Integer, primary_key=True)
    #device_id = Column(Integer, ForeignKey("devices.id"))
    #device = relationship("Device", uselist=False, back_populates='devices')
    #connected_user_id = 0

#    def __repr__(self):
#        return ""
