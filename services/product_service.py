from decimal import Decimal
from typing import List

from django.utils import timezone

from db.price_dao import PriceDAO
from services.image_service import ImageService
from utils.date import get_month_from_range, get_date_year_ago


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


class ProductPriceHistoryService:
    @staticmethod
    def get_product_price_history(product_id):
        price_records = PriceDAO.get_product_price_history(product_id)
        price_records = dict((row['month'].strftime("%Y-%m-%d"), round(row['avg_price'], 2)) for row in price_records)

        all_months_dict = get_month_from_range(get_date_year_ago(), timezone.now())

        for month in all_months_dict.keys():
            all_months_dict[month] = price_records.get(month)

        all_months_dict = ProductPriceHistoryService.__trunc_empty_months(all_months_dict)
        all_months_dict = ProductPriceHistoryService.__interpolate_price(all_months_dict)
        all_months_dict = ProductPriceHistoryService.__expand_price_dict(all_months_dict)
        return all_months_dict

    @staticmethod
    def __expand_price_dict(price_dict_by_months):
        if len(price_dict_by_months.keys()) == 1:
            price_dict_by_months[timezone.now().strftime('%Y-%m-%d')] = next(iter(price_dict_by_months.values()))
        return price_dict_by_months

    @staticmethod
    def __interpolate_price(price_dict_by_months):
        empty_months = []
        left_price, right_price = 0, 0
        for key, value in price_dict_by_months.items():
            if value:
                if len(empty_months) == 0:
                    left_price = value
                elif len(empty_months) > 0:
                    right_price = value
                    step = (right_price - left_price) / (len(empty_months) + 1)
                    for month in empty_months:
                        left_price += step
                        price_dict_by_months[month] = round(left_price, 2)
                    empty_months = []
                    left_price = right_price
            else:
                empty_months.append(key)
        return price_dict_by_months

    @staticmethod
    def __trunc_empty_months(price_dict_by_months):
        truncated_dict = {}
        for key, value in price_dict_by_months.items():
            if value or truncated_dict:
                truncated_dict[key] = value
        return truncated_dict
