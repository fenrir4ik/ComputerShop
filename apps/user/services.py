from apps.user.models import User


def get_user_by_field_value(field_name: str, field_value: str) -> User:
    """Get single user instance by given field name and field value"""
    return User.objects.get(**{field_name: field_value})
