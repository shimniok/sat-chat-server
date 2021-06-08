import re
from flask import current_app
from datetime import datetime
from user import get_user_by_id
from api.models import Notification, rock7_date_format, standard_phone_format, db
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

message_template = "new message on https://satchat.geodexters.us/"


def phone_to_twilio_format(phone):
    """ 
    Convert phone from NNN-NNN-NNNN to twilio format:
    +1NNNNNNNNNN (assumes US numbers only)
    """
    pattern = re.compile(standard_phone_format)
    if pattern.match(phone):
        phone = "+1" + phone
        return phone.replace('-', '')
    else:
        return None


def notify_user(user_id):
    me = get_user_by_id(user_id)
    from_phone = current_app.config['TWILIO_PHONE']
    client = Client(current_app.config['TWILIO_ACCOUNT_SID'],
                    current_app.config['TWILIO_AUTH_TOKEN'])

    return client.messages.create(
        body=message_template,
        to=phone_to_twilio_format(me.phone),
        from_=from_phone
    )
