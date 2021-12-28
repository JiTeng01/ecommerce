from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.conf import settings
from toolbox.utilities.datetime import now
from math import fabs


def check_expiry(login_url=None, is_required=True):
    """
    Decorator for views that checks whether a user has an expired token, redirecting to the log-in page if necessary.
    If the expiry time is more than 2 times of AUTH_VALID_DURATION minutes, redirecting to login page.
    If the expiry time is less than 2 times of AUTH_VALID_DURATION minutes, renewing a new token.
    """
    def check_token(user):

        if isinstance(user, get_user_model()):
            if user.expiry_time and user.expiry_time > now():
                return True

            if user.expiry_time and fabs((user.expiry_time - now()).total_seconds()) <= settings.AUTH_VALID_DURATION * 60:
                user.extend_expiry()
                return True
        else:
            if is_required is False:
                return True

        return False

    return user_passes_test(check_token, login_url=login_url)

