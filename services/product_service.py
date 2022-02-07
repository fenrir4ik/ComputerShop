from abc import ABC
from decimal import Decimal
from typing import List

from apps.store.models import Product
from services.dao.price_dao import PriceDAO
from services.image_manager import ImageManager


class BaseProductService(ABC):
    def __init__(self, instance: Product = None):
        if instance is None:
            raise ValueError("Missing product instance in constructor")
        elif not isinstance(instance, Product):
            raise ValueError(f"Instance should be of type {Product}, but type {type(instance)} given")
        self.product = instance


class ProductService(BaseProductService):
    def add_additional_data(self, price: Decimal, image_list: List[dict]):
        PriceDAO.create_product_price(self.product, price)
        ImageManager.add_product_images(self.product, image_list)

    def update_additional_data(self, price: Decimal, image_list: List[dict]):
        PriceDAO.update_product_price(self.product, price)
        ImageManager.update_product_images(self.product, image_list)
