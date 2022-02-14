from django.db import transaction
from django.db.models import F

from apps.store.models import CartItem, Product
from services.dao.order_dao import OrderDAO


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
            CartItem.objects.filter(order_id=cart_id, product_id=product_id).update(amount=F('amount') + amount_difference)
            Product.objects.filter(pk=product_id).update(amount=F('amount') - amount_difference)

    @staticmethod
    def delete_product_in_cart(cart_id: int, product_id: int):
        with transaction.atomic():
            cart_item = CartItem.objects.filter(order_id=cart_id, product_id=product_id).select_for_update().first()
            Product.objects.filter(pk=product_id).update(amount=F('amount') + cart_item.amount)
            cart_item.delete()
