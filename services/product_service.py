from abc import ABC
from decimal import Decimal

from apps.store.models import Product, ProductPrice
from services.image_manager import ImageManager


class BaseProductService(ABC):
    def __init__(self, instance: Product = None):
        if instance is None:
            raise ValueError("Missing product instance in constructor")
        elif not isinstance(instance, Product):
            raise ValueError(f"Instance should be of type {Product}, but type {type(instance)} given")
        self.product = instance


class ProductService(BaseProductService):
    def __init__(self, instance: Product = None):
        super().__init__(instance)
        self.image_manager = ImageManager()

    def _update_product_price(self, price: Decimal):
        old_price_instance = ProductPrice.objects.filter(product=self.product).order_by('-date_actual').first()
        if old_price_instance.price != price:
            ProductPrice(product=self.product, price=price).save()

    def _save_product_price(self, price: Decimal):
        ProductPrice(product=self.product, price=price).save()

    def add_additional_data(self, price: Decimal, image_list):
        self._save_product_price(price)
        self.image_manager.add_product_images(self.product, image_list)

    def update_additional_data(self, price: Decimal, image_list):
        self._update_product_price(price)
        self.image_manager.update_product_images(self.product, image_list)
