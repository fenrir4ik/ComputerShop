from decimal import Decimal
from typing import List, Dict

from django.utils import timezone

from db.price_dao import PriceDAO
from services.characteristic_service import CharacteristicService
from services.image_service import ImageService
from utils.date import get_month_from_range


class AdditionalProductDataService:
    """Service for managing additional product data: price and image"""

    @staticmethod
    def add_additional_data(product_id: int, price: Decimal, image_list: List[dict], characteristics: List[Dict]):
        PriceDAO.create_product_price(product_id, price)
        ImageService.add_product_images(product_id, image_list)
        CharacteristicService.add_product_characteristics(product_id, characteristics)

    @staticmethod
    def update_additional_data(product_id: int, price: Decimal, image_list: List[dict], characteristics: List[Dict]):
        PriceDAO.update_product_price(product_id, price)
        ImageService.update_product_images(product_id, image_list)
        if characteristics:
            CharacteristicService.update_product_characteristics(product_id, characteristics)


class ProductPriceHistoryService:
    """Service for managing product prices and its history"""

    @staticmethod
    def get_yearly_price_history(product_id: int):
        price_records = PriceDAO.get_product_price_history_by_id(product_ids=[product_id],
                                                                  aggregation_period = 'month',
                                                                  date_start=timezone.now() - timezone.timedelta(days=365))
        price_records = dict((row['period'].strftime("%Y-%m-%d"), round(row['avg_price'], 2)) for row in price_records)

        all_months_dict = get_month_from_range(timezone.now() - timezone.timedelta(days=365), timezone.now())

        for month in all_months_dict.keys():
            all_months_dict[month] = price_records.get(month)

        all_months_dict = ProductPriceHistoryService.__trunc_empty_months(all_months_dict)
        all_months_dict = ProductPriceHistoryService.__interpolate_price(all_months_dict)
        all_months_dict = ProductPriceHistoryService.__expand_price_dict(all_months_dict)
        return all_months_dict

    @staticmethod
    def __expand_price_dict(aggregated_price):
        if len(aggregated_price.keys()) == 1:
            aggregated_price[timezone.now().strftime('%Y-%m-%d')] = next(iter(aggregated_price.values()))
        return aggregated_price

    @staticmethod
    def __interpolate_price(aggregated_price):
        empty_months = []
        left_price, right_price = 0, 0
        month_n = 0
        for key, value in aggregated_price.items():
            month_n += 1
            if value:
                if len(empty_months) == 0:
                    left_price = value
                elif len(empty_months) > 0:
                    right_price = value
                    step = (right_price - left_price) / (len(empty_months) + 1)
                    for month in empty_months:
                        left_price += step
                        aggregated_price[month] = round(left_price, 2)
                    empty_months = []
                    left_price = right_price
            else:
                empty_months.append(key)
                if month_n == len(aggregated_price):
                    for month in empty_months:
                        aggregated_price[month] = round(left_price, 2)
        return aggregated_price

    @staticmethod
    def __trunc_empty_months(aggregated_price):
        truncated_dict = {}
        for key, value in aggregated_price.items():
            if value or truncated_dict:
                truncated_dict[key] = value
        return truncated_dict
