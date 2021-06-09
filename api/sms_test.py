from datetime import datetime, timedelta
import json
from test_fixture import application, client, user1, shared_data
from sms import phone_to_twilio_format, notify_user, get_latest_notification
from api.models import rock7_date_format, Notification, db
from twilio.base.exceptions import TwilioRestException

# Test SMS Phone Numbers:
#
# Test phone numbers From:
#
# +15005550001 	This phone number is invalid. 	21212
# +15005550006 	This number passes all validation. 	No error
# +15005550007 	This phone number is not owned by your account or is not SMS-capable. 	21606
# +15005550008 	This number has an SMS message queue that is full. 	21611
#
# Test Phone Numbers To:
# +15005550001 	This phone number is invalid. 	21211
# +15005550002 	Twilio cannot route to this number. 	21612
# +15005550003 	Your account doesn't have the international permissions necessary to SMS this number. 	21408
# +15005550004 	This number is blocked for your account. 	21610
# +15005550009 	This number is incapable of receiving SMS messages. 	21614

numbers = {
    "+15005550001", 
    "+15005550002",
    "+15005550003",
    "+15005550004",
    "+15005550009",
    "+5571981265131",
}

def test_latest_time(user1):
    now = datetime.utcnow()
    prev_1 = now - timedelta(minutes=16)
    n1 = Notification(user_id=shared_data['user1_id'], time=prev_1)
    db.session.add(n1)
    db.session.commit()
    latest = get_latest_notification(shared_data['user1_id'])

    assert latest != None
    assert latest.time == n1.time
    
    prev_2 = now - timedelta(minutes=14)
    n2 = Notification(user_id=shared_data['user1_id'], time=prev_2)
    db.session.add(n2)
    db.session.commit()
    latest = get_latest_notification(shared_data['user1_id'])
    
    assert latest != None
    assert latest.time == n2.time
    
    db.session.delete(n1)
    db.session.commit()
    
    
def test_send(user1):
    response = notify_user(shared_data['user1_id']) 
    # send_message(message="test", to_phone="+5571981265131")
    assert response != None
    assert response.sid != None
    
    
def test_to_twilio(user1):
    assert phone_to_twilio_format("123-456-7890") == "+11234567890"
    assert phone_to_twilio_format("1234567890") == None
    assert phone_to_twilio_format("1-123-456-7890") == None

    
    # notification1 = Notification(user_id=shared_data['user1'].id,
    #                             time=""))
