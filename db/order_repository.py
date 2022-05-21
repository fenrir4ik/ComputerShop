from django.apps import apps
from django.db.models import QuerySet, Prefetch, Sum, Subquery, F, OuterRef

from db.product_repository import ProductRepository


class OrderRepository:
    def __init__(self):
        self.Order = apps.get_model('store', 'Order')
        self.CartItem = apps.get_model('store', 'CartItem')

    def get_user_cart_id(self, user_id: int) -> int:
        """Returns id of user cart"""
        cart, _ = self.Order.objects.get_or_create(user_id=user_id, status=None)
        return cart.pk

    def get_all_orders(self, user_id: int = None) -> QuerySet:
        """
        Returns all user orders in system
        If user_id is specified, then it returns orders for particular user
        """
        product_repository = ProductRepository()
        cart_items = self.CartItem.objects.select_related('product')
        cart_items = product_repository.annotate_queryset_with_price(cart_items, ref='product_id', actual=False)
        cart_items = product_repository.annotate_queryset_with_image(cart_items, ref='product_id')

        total_price = cart_items.values('order_id') \
            .annotate(total_price=Sum(F('price') * F('amount'))) \
            .filter(order_id=OuterRef('id'))

        user_orders = self.Order.objects.all()
        if user_id:
            user_orders = user_orders.filter(user_id=user_id)

        user_orders = user_orders.exclude(status__isnull=True) \
            .select_related('status', 'payment') \
            .prefetch_related(Prefetch('products', queryset=cart_items)) \
            .annotate(order_total=Subquery(total_price.values('total_price')[:1]))
        return user_orders
