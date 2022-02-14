from django.db import transaction

from services.dao.cart_item_dao import CartItemDAO


class CartService:
    def process_cart_item(self, user_id: int, product_id: int, amount: int):
        with transaction.atomic():
            product_amount_in_cart = CartItemDAO.get_product_amount_in_cart(user_id, product_id)
            if product_amount_in_cart == 0:
                self._add_product_to_cart(user_id, product_id, amount)
            elif amount != product_amount_in_cart:
                self._change_product_in_cart(user_id, product_id, amount - product_amount_in_cart)

    def delete_product_from_cart(self, user_id, product_id):
        with transaction.atomic():
            CartItemDAO.delete_product_in_cart(user_id, product_id)

    def _add_product_to_cart(self, user_id: int, product_id: int, amount: int):
        CartItemDAO.add_product_to_cart(user_id, product_id, amount)

    def _change_product_in_cart(self, user_id: int, product_id: int, amount_difference: int):
        """amount_difference is positive when product amount in cart is less then product amount submitted"""
        CartItemDAO.change_product_in_cart(user_id, product_id, amount_difference)
