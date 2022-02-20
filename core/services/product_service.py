from decimal import Decimal
from typing import List

from core.db.price_dao import PriceDAO
from core.services.image_service import ImageService


class ProductService:
    @staticmethod
    def add_additional_data(product_id: int, price: Decimal, image_list: List[dict]):
        PriceDAO.create_product_price(product_id, price)
        ImageService.add_product_images(product_id, image_list)

    @staticmethod
    def update_additional_data(product_id: int, price: Decimal, image_list: List[dict]):
        PriceDAO.update_product_price(product_id, price)
        ImageService.update_product_images(product_id, image_list)
