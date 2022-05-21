import numpy as np
from django.db.models import QuerySet
from django.utils import timezone

from db.cart_item_repository import CartItemRepository
from db.product_repository import ProductRepository
from db.recommender_repository import RecommenderRepository
from services.product_service import SalesHistoryProcessor, PriceHistoryProcessor
from services.settings import REC_START, REC_PERIOD, REC_DEFAULT_CORRELATION, REC_SOFTSIGN_H
from utils.date import get_periods_from_range


def get_linear_approx_k(x: np.ndarray, y: np.ndarray) -> float:
    """Returns coefficient k for line that approximate given plane graph"""
    if len(x) != len(y):
        raise ValueError(f"Length of x axis doesn't match y axis: {len(x)} != {len(y)}")
    N = len(x)
    k = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / (N * np.sum(x ** 2) - np.sum(x) ** 2)
    return k


def get_price_sales_correlation(price: np.ndarray, sales: np.ndarray):
    matrix = np.corrcoef(price, sales)
    return matrix[0, 1]


def get_sales_growth_speed(k_coefficient: float) -> float:
    k_coefficient = k_coefficient / REC_SOFTSIGN_H

    def soft_sign(x):
        return x / 1 + abs(x)

    return soft_sign(k_coefficient)


class RecommenderService:
    def __init__(self):
        self.distributed_dates = get_periods_from_range(REC_START, timezone.now(), period=REC_PERIOD)

    def process_cart_items(self, cart_id: int):
        cart_products = list(CartItemRepository().get_cart_products_id(cart_id))
        products_price_history = RecommenderRepository().get_price_history(*cart_products)
        products_sales_history = RecommenderRepository().get_sales_history(*cart_products)
        products_price_history = self.__divide_history_by_products(products_price_history,
                                                                   data_field_name='avg_price')
        products_sales_history = self.__divide_history_by_products(products_sales_history,
                                                                   data_field_name='total_products')

        for product_id in cart_products:
            product_prices = products_price_history.get(product_id)
            product_sales = products_sales_history.get(product_id)
            product_prices, product_sales = self.__get_formatted_data(product_prices, product_sales)
            rating_update = self.evaluate_rating_update(product_prices, product_sales)
            if rating_update != 0.0:
                ProductRepository().update_product_rating(product_id, rating_update)

    def __divide_history_by_products(self,
                                     qs: QuerySet,
                                     pk_field_name: str = 'product_id',
                                     period_field_name: str = 'period',
                                     data_field_name: str = None) -> dict:
        """Parses given qs to format suitable for future processing"""

        parsed_data = {}
        for row in qs:
            key = row.get(pk_field_name)
            parsed_data.setdefault(key, {})
            parsed_data[key][row.get(period_field_name).strftime("%Y-%m-%d")] = row.get(data_field_name)
        return parsed_data

    def evaluate_rating_update(self, price_data: np.ndarray, sales_data: np.ndarray) -> float:
        if sales_data is None:
            return 0.0
        else:
            time_range = np.linspace(0, 1, num=len(sales_data))
        k = get_linear_approx_k(time_range, sales_data)
        if k == 0:
            return 0.0
        if price_data is None or np.min(price_data) == np.max(price_data) or np.min(sales_data) == np.max(sales_data):
            correlation = REC_DEFAULT_CORRELATION
        else:
            correlation = get_price_sales_correlation(price_data, sales_data)
        v = get_sales_growth_speed(k)
        rating_update = abs(correlation) * v
        return rating_update

    def __get_formatted_data(self, price_data: dict, sales_data: dict) -> tuple:
        price, sales = None, None
        if price_data is not None:
            price = PriceHistoryProcessor().process_price_history(self.distributed_dates, price_data)
            price = np.array(list(price.values()), dtype=np.float32)
        if sales_data is not None:
            sales = SalesHistoryProcessor().process_sales_history(self.distributed_dates, sales_data)
            sales = np.array(list(sales.values()), dtype=np.int)
        return price, sales
