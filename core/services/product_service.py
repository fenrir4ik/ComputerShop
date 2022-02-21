from decimal import Decimal
from typing import List

from core.db.price_dao import PriceDAO
from core.services.image_service import ImageService


class AdditionalProductDataService:
    """Service for managing additional product data: price and image"""

    @staticmethod
    def add_additional_data(product_id: int, price: Decimal, image_list: List[dict]):
        """Method takes in product id, new price and image_list and creates price and image instances in database"""
        PriceDAO.create_product_price(product_id, price)
        ImageService.add_product_images(product_id, image_list)

    @staticmethod
    def update_additional_data(product_id: int, price: Decimal, image_list: List[dict]):
        """Method takes in product id, new price and image_list and updates price and image instances"""
        PriceDAO.update_product_price(product_id, price)
        ImageService.update_product_images(product_id, image_list)
