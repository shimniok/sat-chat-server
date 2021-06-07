from user import get_user_by_id
from api.models import User

class sms:
    def __init__(self):
        return

    def notify_user(self, user):
        print("name={} phone={}", user.name, user.phone)
        return

