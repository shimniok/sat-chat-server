from app import db
from sqlalchemy.dialects.postgresql import JSON

class Message(db.Model):
        __tablename__ = 'messages'

        id = db.Column(db.Integer, primary_key=True)
        #from_user = db.Column(db.String())
        #to_user = db.Column(db.String())
        message = db.Column(db.String())
        #json = db.Column(JSON)
        #momsn = request.form.get('momsn')
        #transmit_time = request.form.get('transmit_time')
        #iridium_latitude = request.form.get('iridium_latitude')
        #iridium_longitude = request.form.get('iridium_longitude')
        #iridium_cep = request.form.get('iridium_cep')
        #text = request.form.get('data')

        def __init__(self, message):
            self.message = message

        def __repr__(self):
            return '<id {}>'.format(self.id)
