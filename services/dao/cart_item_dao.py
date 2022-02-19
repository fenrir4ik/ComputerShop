from typing import Union

from django.db import transaction
from django.db.models import F, OuterRef, Subquery, QuerySet

from apps.store.models import CartItem, Product
from services.dao.order_dao import OrderDAO
from services.dao.product_dao import ProductDAO


class CartItemDAO:
    @staticmethod
    def get_product_amount_in_cart_by_user_id(user_id: int, product_id) -> int:
        cart_id = OrderDAO.get_user_cart_id(user_id)
        return CartItemDAO.get_product_amount_in_cart(cart_id, product_id)

    @staticmethod
    def get_product_amount_in_cart(cart_id: int, product_id: int) -> int:
        try:
            cart_item = CartItem.objects.get(order_id=cart_id, product_id=product_id)
            return cart_item.amount
        except CartItem.DoesNotExist:
            return 0

    @staticmethod
    def add_product_to_cart(cart_id: int, product_id: int, amount: int):
        with transaction.atomic():
            CartItem.objects.create(order_id=cart_id, product_id=product_id, amount=amount)
            Product.objects.filter(pk=product_id).update(amount=F('amount') - amount)

    @staticmethod
    def change_product_in_cart(cart_id: int, product_id: int, amount_difference: int):
        with transaction.atomic():
            CartItem.objects.filter(order_id=cart_id, product_id=product_id).update(
                amount=F('amount') + amount_difference)
            Product.objects.filter(pk=product_id).update(amount=F('amount') - amount_difference)

    @staticmethod
    def delete_products_in_cart(cart_id: int, products_id: Union[int, QuerySet]):
        if isinstance(products_id, int):
            products_id = [products_id]
        else:
            products_id = list(products_id)
        with transaction.atomic():
            cart_item = CartItem.objects.filter(order_id=cart_id, product_id__in=products_id).select_for_update()
            Product.objects.filter(pk__in=products_id) \
                .update(amount=F('amount') + Subquery(cart_item.filter(product_id=OuterRef('pk')).values('amount')))
            cart_item.delete()

    @staticmethod
    def get_user_cart(user_id: int):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        user_cart = CartItem.objects.filter(order_id=cart_id).select_related('product')
        user_cart = ProductDAO.annotate_queryset_with_image(user_cart, ref='product_id')
        user_cart = ProductDAO.annotate_queryset_with_price(user_cart, ref='product_id')
        return user_cart

    @staticmethod
    def clear_cart(cart_id: int):
        products_in_cart = CartItem.objects.filter(order_id=cart_id).values_list('product_id', flat=True)
        CartItemDAO.delete_products_in_cart(cart_id, products_in_cart)
