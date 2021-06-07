from user import get_user_by_id
from api.models import User
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class SMS:
    message_template = "new message on https://satchat.geodexters.us/"
    
    def __init__(self, app):
        self.client = Client(app.config['TWILIO_ACCOUNT_SID'], 
                             app.config['TWILIO_AUTH_TOKEN'])
        self.from_phone = app.config['TWILIO_PHONE']
        return

    def notify_user(self, user):
        print("name={} phone={}", user.name, user.phone)
        self.send_message(self.message_template, user.phone)
        return
    
    def send_message(self, message, to_phone):
        return self.client.messages.create(
            body=message,
            to=to_phone,
            from_=self.from_phone
        )
