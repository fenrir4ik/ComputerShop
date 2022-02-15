from decimal import Decimal
from typing import List

from services.dao.price_dao import PriceDAO
from services.image_manager import ImageManager


class ProductService:
    def add_additional_data(self, product_id: int, price: Decimal, image_list: List[dict]):
        PriceDAO.create_product_price(product_id, price)
        ImageManager.add_product_images(product_id, image_list)

    def update_additional_data(self, product_id: int, price: Decimal, image_list: List[dict]):
        PriceDAO.update_product_price(product_id, price)
        ImageManager.update_product_images(product_id, image_list)
