from apps.store.models import Product, Order


class CartItemDao:
    @staticmethod
    def product_exists_in_user_cart(order: Order, product: Product) -> bool:
        pass

    @staticmethod
    def add_product_to_cart(order: Order, product: Product, amount: int) -> bool:
        pass

    @staticmethod
    def change_product_in_cart(order: Order, product: Product, amount: int) -> bool:
        pass

    @staticmethod
    def delete_product_in_cart(order: Order, product: Product) -> bool:
        pass