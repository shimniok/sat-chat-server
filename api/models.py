from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy, Model
from flask_migrate import Migrate, upgrade
from output_mixin import OutputMixin
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
import binascii
from json_parser import dt_fmt

db = SQLAlchemy()

rock7_date_format = "%y-%m-%d %H:%M:%S"
json_date_format = dt_fmt

#TODO: create roles table, add role Column to each user


def decode_date(dtstr):
    for f in [ rock7_date_format, json_date_format ]:
        try:
            t = datetime.strptime(dtstr, f)
            return t
        except:
            pass
    raise ValueError


def init_db(app):
    db.init_app(app)

    if app.config['TESTING'] == True:
        # initialize test database
        db.create_all()
    else:
        # upgrade the database
        try:
            Migrate(app, db)
            upgrade()
            print("upgrade complete")
        except Exception as e:
            print("db migration failed: {}".format(str(e)))
    
    # insert admin user if doesn't exist
    admin = User.query.filter_by(name='admin').first()
    if not admin:
        admin = User(
            name='admin',
            email='admin@example.com',
            password=generate_password_hash('admin', method='sha256'),
            admin=True
        )
        db.session.add(admin)
        db.session.commit()
    
    if not admin.admin:
        admin.admin = True
        db.session.commit()

    return


class Message(OutputMixin, db.Model):
    __tablename__ = 'messages'
    #TODO: RELATIONSHIPS_TO_DICT = True
    RELATIONSHIPS_TO_DICT = False

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device")
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship("User")
    momsn = Column(Integer)
    message = Column(String())
    transmit_time = Column(DateTime())
    time = Column(DateTime())
    iridium_latitude = Column(Float())
    iridium_longitude = Column(Float())
    iridium_cep = Column(Float())

    def __init__(self, device_id=None, sender_id=None, momsn=-1, message='',
        transmit_time="70-01-01 00:00", time="70-01-01 00:00",
        iridium_latitude=0, iridium_longitude=0, iridium_cep=0):

        self.device_id = device_id
        self.sender_id = sender_id
        self.momsn = momsn
        self.message = message
        try:
            self.transmit_time = decode_date(transmit_time)
            self.time = decode_date(time)
        except ValueError as e:
            print("Message: bad time format: {}".format(e))
        self.iridium_latitude=iridium_latitude
        self.iridium_longitude=iridium_longitude
        self.iridium_cep=iridium_cep


class User(OutputMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    PROTECTED_COLUMNS = [ 'password' ]
    RELATIONSHIPS_TO_DICT = True

    id = Column(Integer, primary_key=True)
    email = Column(String(), unique=True)
    name = Column(String())
    password = Column(String())
    device = relationship("Device", uselist=False, back_populates="owner")
    admin = Column(Boolean())

    def __init__(self, email="", name="", password="", admin=False):
        self.email=email
        self.name=name
        self.password=password
        self.admin=admin


class Device(OutputMixin, db.Model):
    __tablename__ = 'devices'
    #PROTECTED_COLUMNS = [ 'password' ]
    RELATIONSHIPS_TO_DICT = False

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="device")
    imei = Column(String(), unique=True)
    username = Column(String())
    password = Column(String())

    def __init__(self, owner_id, imei, username, password):
        self.owner_id = owner_id
        self.imei = imei
        self.username = username
        self.password = generate_password_hash(username, method='sha256')

