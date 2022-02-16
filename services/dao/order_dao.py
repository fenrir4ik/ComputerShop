from django.db.models import QuerySet, Prefetch

from apps.store.models import Order, CartItem
from services.dao.product_dao import ProductDAO


class OrderDAO:
    @staticmethod
    def get_user_cart_id(user_id: int) -> int:
        cart, _ = Order.objects.get_or_create(user_id=user_id, status=None)
        return cart.pk

    @staticmethod
    def get_user_orders(user_id: int) -> QuerySet:
        cart_items = CartItem.objects.select_related('product')
        cart_items = ProductDAO.annotate_queryset_with_price(cart_items, ref='product_id')
        cart_items = ProductDAO.annotate_queryset_with_image(cart_items, ref='product_id')
        user_orders = Order.objects.filter(user_id=user_id).\
            exclude(status__isnull=True).\
            select_related('status', 'payment').\
            prefetch_related(Prefetch('products', queryset=cart_items))
        return user_orders
