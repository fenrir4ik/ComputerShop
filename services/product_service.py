from decimal import Decimal
from typing import List

from apps.store.models import Product
from services.base_service import BaseService
from services.dao.price_dao import PriceDAO
from services.image_manager import ImageManager


class ProductService(BaseService):
    instance_class = Product

    def add_additional_data(self, price: Decimal, image_list: List[dict]):
        PriceDAO.create_product_price(self.instance, price)
        ImageManager.add_product_images(self.instance, image_list)

    def update_additional_data(self, price: Decimal, image_list: List[dict]):
        PriceDAO.update_product_price(self.instance, price)
        ImageManager.update_product_images(self.instance, image_list)
