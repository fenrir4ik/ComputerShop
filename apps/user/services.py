from apps.user.models import User


def get_user_by_field_value(field_name: str, field_value: str) -> User:
    """
    Returns a user by given field and value
    :param str field_name: field to search
    :param str field_value: value to search
    :return: user instance
    """
    return User.objects.get(**{field_name: field_value})
