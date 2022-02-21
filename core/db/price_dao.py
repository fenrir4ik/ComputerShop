from decimal import Decimal

from apps.store.models import ProductPrice


class PriceDAO:
    """DAO is used to interact with ProductPrice model instances"""

    @staticmethod
    def update_product_price(product_id: int, price: Decimal):
        """
        Updates price of given product
        This method is used during product update
        Product price history will be formed as a result of multiple price updates
        """
        old_price_instance = ProductPrice.objects.filter(product_id=product_id).order_by('-date_actual').first()
        if old_price_instance.price != price:
            PriceDAO.create_product_price(product_id, price)

    @staticmethod
    def create_product_price(product_id: int, price: Decimal):
        """
        Creates product price instance in the db for given product
        It's used during initial product creation
        """
        ProductPrice(product_id=product_id, price=price).save()
