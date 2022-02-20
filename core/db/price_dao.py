from decimal import Decimal

from apps.store.models import ProductPrice


class PriceDao:
    @staticmethod
    def update_product_price(product_id: int, price: Decimal):
        old_price_instance = ProductPrice.objects.filter(product_id=product_id).order_by('-date_actual').first()
        if old_price_instance.price != price:
            PriceDao.create_product_price(product_id, price)

    @staticmethod
    def create_product_price(product_id: int, price: Decimal):
        ProductPrice(product_id=product_id, price=price).save()
