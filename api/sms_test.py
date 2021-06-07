from flask import current_app
from test_fixture import application, client, user1, shared_data
from sms import SMS
import json
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


def test_send(user1):
    sms = SMS(current_app)
    assert sms != None
    response = sms.send_message(
        message="test", to_phone="+5571981265131")
    assert response.sid != None

