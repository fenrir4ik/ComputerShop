from apps.user.models import User


class UserDAO:
    @staticmethod
    def get_user_by_email(email: str) -> User:
        """Get single user instance by given email"""
        return User.objects.get(email__iexact=email)
