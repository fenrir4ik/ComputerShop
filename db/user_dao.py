from typing import Union

from apps.user.models import User


class UserDAO:
    """DAO is used to interact with User model instances"""

    @staticmethod
    def get_user_by_username(username: str) -> Union[User, None]:
        """Get single user instance by given email"""
        try:
            return User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None
