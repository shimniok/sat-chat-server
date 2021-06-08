from flask import current_app
from datetime import datetime
from user import get_user_by_id
from api.models import Notification, rock7_date_format, db
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

message_template = "new message on https://satchat.geodexters.us/"

from_phone = current_app.config['TWILIO_PHONE']
client = Client(current_app.config['TWILIO_ACCOUNT_SID'],
                current_app.config['TWILIO_AUTH_TOKEN'])

def notify_user(user_id):
    me = get_user_by_id(user_id)
    
    try:
        client.messages.create(
            body=message_template,
            to=me.phone,
            from_=from_phone
        )
    except Exception:
        pass
