from apps.user.models import User


def find_user_by_email(email: str) -> User:
    """Get single user instance by given email"""
    return User.objects.get(email__iexact=email)
