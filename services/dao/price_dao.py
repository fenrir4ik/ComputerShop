from decimal import Decimal

from apps.store.models import ProductPrice, Product


class PriceDAO:
    @staticmethod
    def update_product_price(product: Product, price: Decimal):
        old_price_instance = ProductPrice.objects.filter(product=product).order_by('-date_actual').first()
        if old_price_instance.price != price:
            PriceDAO.create_product_price(product, price)

    @staticmethod
    def create_product_price(product: Product, price: Decimal):
        ProductPrice(product=product, price=price).save()
