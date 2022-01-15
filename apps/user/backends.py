from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class PhoneEmailBasedBackend(ModelBackend):
    """Authenticate user against given email address OR phone number
       Returns user with given credentials or none if user not found
       or password is wrong"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(phone_number=username))
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
