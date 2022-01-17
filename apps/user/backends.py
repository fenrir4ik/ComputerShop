from django.contrib.auth.backends import ModelBackend

from apps.user.models import User
from apps.user.services import find_user_by_email


class PhoneEmailBasedBackend(ModelBackend):
    """Authenticate user against given email address and password"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = find_user_by_email(username)
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
