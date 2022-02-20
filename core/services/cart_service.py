from core.db.cart_item_dao import CartItemDao
from core.db.order_dao import OrderDao


class CartService:
    @staticmethod
    def process_cart_item(user_id: int, product_id: int, amount: int):
        cart_id = OrderDao.get_user_cart_id(user_id)
        product_amount_in_cart = CartItemDao.get_product_amount_in_cart(cart_id, product_id)
        if product_amount_in_cart == 0:
            CartService.__add_product_to_cart(cart_id, product_id, amount)
        elif amount != product_amount_in_cart:
            CartService._change_product_in_cart(cart_id, product_id, amount - product_amount_in_cart)

    @staticmethod
    def delete_product_from_cart(user_id, product_id):
        cart_id = OrderDao.get_user_cart_id(user_id)
        CartItemDao.delete_products_in_cart(cart_id, product_id)

    @staticmethod
    def __add_product_to_cart(cart_id: int, product_id: int, amount: int):
        CartItemDao.add_product_to_cart(cart_id, product_id, amount)

    @staticmethod
    def _change_product_in_cart(cart_id: int, product_id: int, amount: int):
        CartItemDao.change_product_in_cart(cart_id, product_id, amount)

    @staticmethod
    def clear_user_cart(user_id):
        cart_id = OrderDao.get_user_cart_id(user_id)
        CartItemDao.clear_cart(cart_id)
