from django.contrib.auth.backends import ModelBackend

from apps.user.models import User
from services.dao.user_dao import UserDAO


class EmailBasedBackend(ModelBackend):
    """Authenticate user against given email address and password"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserDAO.get_user_by_email(username)
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
