from django.db.models import QuerySet, Prefetch, Sum, Subquery, F, OuterRef

from apps.store.models import Order, CartItem
from db.product_dao import ProductDAO


class OrderDAO:
    """DAO is used to interact with Order model instances"""

    @staticmethod
    def get_user_cart_id(user_id: int) -> int:
        """Returns id of user cart"""
        cart, _ = Order.objects.get_or_create(user_id=user_id, status=None)
        return cart.pk

    @staticmethod
    def get_all_orders(user_id: int = None) -> QuerySet:
        """
        Returns all user orders in system
        If user_id is specified, then it returns orders for particular user
        """
        cart_items = CartItem.objects.select_related('product')
        cart_items = ProductDAO.annotate_queryset_with_price(cart_items, ref='product_id', actual=False)
        cart_items = ProductDAO.annotate_queryset_with_image(cart_items, ref='product_id')

        total_price = cart_items.values('order_id') \
            .annotate(total_price=Sum(F('price') * F('amount'))) \
            .filter(order_id=OuterRef('id'))

        user_orders = Order.objects.all()
        if user_id:
            user_orders = user_orders.filter(user_id=user_id)

        user_orders = user_orders.exclude(status__isnull=True) \
            .select_related('status', 'payment') \
            .prefetch_related(Prefetch('products', queryset=cart_items)) \
            .annotate(order_total=Subquery(total_price.values('total_price')[:1]))
        return user_orders
