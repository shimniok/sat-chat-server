import re
from flask import current_app
from datetime import datetime
from api.user import get_user_by_id
from api.models import Notification, rock7_date_format, standard_phone_format, db
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

NOTIFY_INTERVAL_MINUTES = 15

def phone_to_twilio_format(phone):
    """ 
    Convert phone from NNN-NNN-NNNN to twilio format +1NNNNNNNNNN (assumes US numbers only)
    """
    pattern = re.compile(standard_phone_format)
    if pattern.match(phone):
        phone = "+1" + phone
        return phone.replace('-', '')
    else:
        return None


def get_latest_notification(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).order_by(
        Notification.time.desc()).all()
    if notifications == None or len(notifications) == 0:
        return None
    return notifications[0]


def log_notification(user_id):
    now = datetime.utcnow()
    n = Notification(user_id=user_id, time=now)
    db.session.add(n)
    db.session.commit()


def notification_interval_exceeded(user_id):
    result = False
    now = datetime.strftime(datetime.utcnow(), rock7_date_format)
    latest = get_latest_notification(user_id)
    if not latest == None:
        n = get_latest_notification(user_id)
        elapsed = datetime.utcnow() - n.time
        if elapsed.total_seconds()/60 > NOTIFY_INTERVAL_MINUTES:
            result = True
    else:
        result = True

    return result


def notify_user(user_id, text):
    me = get_user_by_id(user_id)
    from_phone = current_app.config['TWILIO_PHONE']
    client = Client(current_app.config['TWILIO_ACCOUNT_SID'],
                    current_app.config['TWILIO_AUTH_TOKEN'])

    response = client.messages.create(
        body=text,
        to=phone_to_twilio_format(me.phone),
        from_=from_phone
    )
    
    if response != None:
        log_notification(user_id)
    
    return response
