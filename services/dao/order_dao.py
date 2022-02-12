from apps.store.models import Order
from apps.user.models import User


class OrderDao:
    @staticmethod
    def get_user_cart(user: User) -> Order:
        pass

    @staticmethod
    def _create_user_cart(user: User) -> Order:
        pass