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


class PriceHistoryChartService:
    """Service for managing product prices and its history"""

    def get_product_price_history(self, product_id: int):
        price_repository = PriceRepository()
        price_records = price_repository.get_product_price_history_by_id(product_id,
                                                                         aggregation_period=PH_PERIOD,
                                                                         date_start=PH_START)
        price_records = dict((row['period'].strftime("%Y-%m-%d"), round(row['avg_price'], 2)) for row in price_records)
        distributed_dates = get_periods_from_range(PH_START, timezone.now(), period=PH_PERIOD)
        if not price_records:
            price_records[next(iter(distributed_dates.keys()))] = price_repository.get_last_product_price(product_id)
        price_history_service = PriceHistoryProcessor()
        aggregated_price = price_history_service.process_price_history(distributed_dates, price_records)
        aggregated_price = price_history_service.expand_price_period(aggregated_price)
        return aggregated_price


class PriceHistoryProcessor:
    """Service for processing price history retrieved from database"""

    def process_price_history(self, distributed_dates: dict, price_records: dict):
        aggregated_price = self.__refill_all_periods(distributed_dates, price_records)
        aggregated_price = self.__define_first_period(aggregated_price)
        aggregated_price = self.__interpolate_price(aggregated_price)
        return aggregated_price

    def __refill_all_periods(self, distributed_dates: dict, price_records: dict):
        """
        Converts price_records which is dict (key: period, value: average_price for given period)
        Into distributed_dates which contains all periods
        If period is not in price_records, the average price is set to None
        """
        result_dates = distributed_dates.copy()
        for period in result_dates.keys():
            result_dates[period] = price_records.get(period)
        return result_dates

    def __define_first_period(self, aggregated_price: dict):
        """
        If first period of sales history is None, it should be defined as first period in dictionary which is not None
        """
        result_price = aggregated_price.copy()
        first_period = next(iter(result_price.keys()))
        for key, value in result_price.items():
            if result_price[first_period]:
                break
            else:
                if value:
                    result_price[first_period] = value
        return result_price

    def __interpolate_price(self, aggregated_price: dict):
        """
        Performs interpolating price inside price history
        """
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

    def expand_price_period(self, aggregated_price):
        """
        For creating chart there should be 2 periods or more
        """
        result_price = aggregated_price.copy()
        if len(result_price.keys()) == 1:
            result_price[timezone.now().strftime('%Y-%m-%d')] = next(iter(result_price.values()))
        return result_price


class SalesHistoryProcessor:
    """Service for processing sales history retrieved from database"""

    def process_sales_history(self, distributed_dates: dict, sales_records: dict):
        """
        Sales records may not contain sales for given period
        As a result sales history returned for every period, and if there is no sales for given period it is set to 0
        """
        result_sales = distributed_dates.copy()
        for key in result_sales.keys():
            result_sales[key] = sales_records.get(key, 0)
        return result_sales
