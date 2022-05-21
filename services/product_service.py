from decimal import Decimal
from typing import List, Dict

from django.utils import timezone

from db.price_repository import PriceRepository
from services.characteristic_service import CharacteristicService
from services.image_service import ImageService
from services.settings import PH_START, PH_PERIOD
from utils.date import get_periods_from_range


class AdditionalProductDataService:
    """Service for managing additional product data: price and image"""

    def add_additional_data(self, product_id: int, price: Decimal, image_list: List[dict], characteristics: List[Dict]):
        PriceRepository().create_product_price(product_id, price)
        ImageService().add_product_images(product_id, image_list)
        CharacteristicService().add_product_characteristics(product_id, characteristics)

    def update_additional_data(self, product_id: int, price: Decimal, image_list: List[dict],
                               characteristics: List[Dict]):
        PriceRepository().update_product_price(product_id, price)
        ImageService().update_product_images(product_id, image_list)
        if characteristics:
            CharacteristicService().update_product_characteristics(product_id, characteristics)


class PriceHistoryService:
    """Service for managing product prices and its history"""

    @staticmethod
    def get_single_product_price_history(product_id: int):
        price_repository = PriceRepository()
        price_records = price_repository.get_product_price_history_by_id([product_id],
                                                                         aggregation_period=PH_PERIOD,
                                                                         date_start=PH_START)
        price_records = dict((row['period'].strftime("%Y-%m-%d"), round(row['avg_price'], 2)) for row in price_records)
        distributed_dates = get_periods_from_range(PH_START, timezone.now(), period=PH_PERIOD)
        if not price_records:
            price_records[next(iter(distributed_dates.keys()))] = price_repository.get_last_product_price(product_id)
        aggregated_price = PriceHistoryService.process_price_history(distributed_dates, price_records)
        aggregated_price = PriceHistoryService.__expand_price_dict(aggregated_price)
        return aggregated_price

    @staticmethod
    def process_price_history(distributed_dates: dict, price_records: dict):
        aggregated_price = PriceHistoryService.__refill_all_periods(distributed_dates, price_records)
        aggregated_price = PriceHistoryService.__define_first_period(aggregated_price)
        aggregated_price = PriceHistoryService.__interpolate_price(aggregated_price)
        return aggregated_price

    @staticmethod
    def __refill_all_periods(distributed_dates: dict, price_records: dict):
        result_dates = distributed_dates.copy()
        for period in result_dates.keys():
            result_dates[period] = price_records.get(period)
        return result_dates

    @staticmethod
    def __define_first_period(aggregated_price: dict):
        result_price = aggregated_price.copy()
        first_period = next(iter(result_price.keys()))
        for key, value in result_price.items():
            if result_price[first_period]:
                break
            else:
                if value:
                    result_price[first_period] = value
        return result_price

    @staticmethod
    def __interpolate_price(aggregated_price: dict):
        result_price = aggregated_price.copy()
        empty_periods = []
        left_price, right_price = 0, 0
        period_n = 0
        for key, value in result_price.items():
            period_n += 1
            if value:
                if len(empty_periods) == 0:
                    left_price = value
                elif len(empty_periods) > 0:
                    right_price = value
                    step = (right_price - left_price) / (len(empty_periods) + 1)
                    for period in empty_periods:
                        left_price += step
                        result_price[period] = round(left_price, 2)
                    empty_periods = []
                    left_price = right_price
            else:
                empty_periods.append(key)
                if period_n == len(result_price):
                    for period in empty_periods:
                        result_price[period] = round(left_price, 2)
        return result_price

    @staticmethod
    def __expand_price_dict(aggregated_price):
        result_price = aggregated_price.copy()
        if len(result_price.keys()) == 1:
            result_price[timezone.now().strftime('%Y-%m-%d')] = next(iter(result_price.values()))
        return result_price
