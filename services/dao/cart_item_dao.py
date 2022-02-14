from django.db.models import F

from apps.store.models import CartItem, Product
from services.dao.order_dao import OrderDAO


class CartItemDAO:
    @staticmethod
    def get_product_amount_in_cart(user_id: int, product_id: int) -> int:
        cart_id = OrderDAO.get_user_cart_id(user_id)
        try:
            cart_item = CartItem.objects.get(order_id=cart_id, product_id=product_id)
            return cart_item.amount
        except CartItem.DoesNotExist:
            return 0

    @staticmethod
    def add_product_to_cart(user_id: int, product_id: int, amount: int):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        CartItem.objects.update_or_create(order_id=cart_id, product_id=product_id, amount=amount)
        Product.objects.filter(pk=product_id).update(amount=F('amount') - amount)

    @staticmethod
    def change_product_in_cart(user_id: int, product_id: int, amount_difference: int):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        CartItem.objects.filter(order_id=cart_id, product_id=product_id).update(amount=F('amount') + amount_difference)
        Product.objects.filter(pk=product_id).update(amount=F('amount') - amount_difference)

    @staticmethod
    def delete_product_in_cart(user_id: int, product_id: int):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        cart_item = CartItem.objects.filter(order_id=cart_id, product_id=product_id).select_for_update().first()
        Product.objects.filter(pk=product_id).update(amount=F('amount') + cart_item.amount)
        cart_item.delete()


