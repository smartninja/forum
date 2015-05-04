from google.appengine.api import users
from settings import ADMINS


def user_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()

        if user:
            return handler(self, *args, **kwargs)
        else:
            return self.redirect(users.create_login_url('/'))

    return check_login

def admin_required(handler):
    def check_login(self, *args, **kwargs):
        username = users.get_current_user().nickname()

        if username in ADMINS:
            return handler(self, *args, **kwargs)
        else:
            return self.redirect(users.create_login_url('/'))

    return check_login