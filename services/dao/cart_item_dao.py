class CartItemDao:
    @staticmethod
    def product_exists_in_user_cart(order_id: int, product_id: int) -> bool:
        pass

    @staticmethod
    def add_product_to_cart(order_id: int, product_id: int, amount: int) -> bool:
        pass

    @staticmethod
    def change_product_in_cart(order_id: int, product_id: int, amount: int) -> bool:
        pass

    @staticmethod
    def delete_product_in_cart(order_id: int, product_id: int) -> bool:
        pass