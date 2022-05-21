from typing import Union

from django.apps import apps

from apps.core.models import User


class UserRepository:
    """Repository is used to interact with User model instances"""

    def __init__(self):
        self.User = apps.get_model('user', 'User')

    def get_user_by_email(self, email: str) -> Union[User, None]:
        """Get single user instance by given email"""
        try:
            return self.User.objects.get(email__iexact=email)
        except self.User.DoesNotExist:
            return None
