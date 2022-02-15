from apps.store.models import Order


class OrderDAO:
    @staticmethod
    def get_user_cart_id(user_id: int) -> int:
        cart, _ = Order.objects.get_or_create(user_id=user_id, status=None)
        return cart.pk
