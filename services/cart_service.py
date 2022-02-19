from services.dao.cart_item_dao import CartItemDAO
from services.dao.order_dao import OrderDAO


class CartService:
    def process_cart_item(self, user_id: int, product_id: int, amount: int):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        product_amount_in_cart = CartItemDAO.get_product_amount_in_cart(cart_id, product_id)
        if product_amount_in_cart == 0:
            self._add_product_to_cart(cart_id, product_id, amount)
        elif amount != product_amount_in_cart:
            self._change_product_in_cart(cart_id, product_id, amount - product_amount_in_cart)

    def delete_product_from_cart(self, user_id, product_id):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        CartItemDAO.delete_products_in_cart(cart_id, product_id)

    def _add_product_to_cart(self, cart_id: int, product_id: int, amount: int):
        CartItemDAO.add_product_to_cart(cart_id, product_id, amount)

    def _change_product_in_cart(self, cart_id: int, product_id: int, amount: int):
        CartItemDAO.change_product_in_cart(cart_id, product_id, amount)

    def clear_user_cart(self, user_id):
        cart_id = OrderDAO.get_user_cart_id(user_id)
        CartItemDAO.clear_cart(cart_id)
