from django.db.models import QuerySet, Prefetch, Sum, Subquery, F, OuterRef

from apps.store.models import Order, CartItem
from services.dao.product_dao import ProductDAO


class OrderDAO:
    @staticmethod
    def get_user_cart_id(user_id: int) -> int:
        cart, _ = Order.objects.get_or_create(user_id=user_id, status=None)
        return cart.pk

    @staticmethod
    def get_all_orders(user_id: int = None) -> QuerySet:
        cart_items = CartItem.objects.select_related('product')
        cart_items = ProductDAO.annotate_queryset_with_price(cart_items, ref='product_id', actual=False)
        cart_items = ProductDAO.annotate_queryset_with_image(cart_items, ref='product_id')
        total_amount = cart_items.values('order_id') \
            .annotate(total_amount=Sum(F('price') * F('amount'))) \
            .filter(order_id=OuterRef('id'))

        user_orders = Order.objects.all()
        if user_id:
            user_orders = user_orders.filter(user_id=user_id)
        user_orders = user_orders.exclude(status__isnull=True) \
            .select_related('status', 'payment') \
            .prefetch_related(Prefetch('products', queryset=cart_items)) \
            .annotate(order_total=Subquery(total_amount.values('total_amount')[:1]))
        return user_orders
