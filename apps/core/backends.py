from django.contrib.auth.backends import ModelBackend

from apps.core.models import User
from db.user_repository import UserRepository


class EmailBasedBackend(ModelBackend):
    """Authenticate user against given email address and password"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = UserRepository().get_user_by_email(username)
        if user and user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
