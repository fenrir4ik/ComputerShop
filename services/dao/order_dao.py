from apps.store.models import Order


class OrderDao:
    @staticmethod
    def get_user_cart(user_id: int) -> Order:
        pass

    @staticmethod
    def _create_user_cart(user_id: int) -> Order:
        pass