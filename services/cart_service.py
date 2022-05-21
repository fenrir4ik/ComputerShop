from db.cart_item_repository import CartItemRepository
from db.order_repository import OrderRepository


class CartService:
    """Service is used for shopping cart managing"""

    def __init__(self, user_id):
        self.cart_id = OrderRepository().get_user_cart_id(user_id)

    def process_cart_item(self, product_id: int, amount: int):
        """
        Method takes in user id, product id and amount
        It finds current product amount in user cart and choose what to do having given amount
        Possible actions: add product to cart, change product amount in cart
        """
        product_amount_in_cart = CartItemRepository().get_product_amount_in_cart(self.cart_id, product_id)
        if product_amount_in_cart == 0:
            self.__add_product_to_cart(product_id, amount)
        elif amount != product_amount_in_cart:
            self.__change_product_in_cart(product_id, amount - product_amount_in_cart)

    def delete_product_from_cart(self, product_id):
        """Deletes product with given id from user cart"""
        CartItemRepository().delete_products_in_cart(self.cart_id, product_id)

    def __add_product_to_cart(self, product_id: int, amount: int):
        """Adds given amount of product with given id to user cart"""
        CartItemRepository().add_product_to_cart(self.cart_id, product_id, amount)

    def __change_product_in_cart(self, product_id: int, amount: int):
        """Changes amount of product with given id in user cart"""
        CartItemRepository().change_product_in_cart(self.cart_id, product_id, amount)
