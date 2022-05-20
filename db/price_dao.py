from decimal import Decimal
from typing import List

from django.db.models import Avg, QuerySet
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay

import apps.store.models as models


class PriceDAO:
    """DAO is used to interact with ProductPrice model instances"""
    aggregation_period_dict = {
        'month': TruncMonth,
        'week': TruncWeek,
        'day': TruncDay
    }

    @staticmethod
    def get_last_product_price(product_id: int):
        return models.ProductPrice.objects.filter(product_id=product_id) \
            .values_list('price', flat=True).order_by('-date_actual')[0]

    @staticmethod
    def update_product_price(product_id: int, price: Decimal):
        """
        Updates price of given product
        This method is used during product update
        Product price history will be formed as a result of multiple price updates
        """
        old_price = PriceDAO.get_last_product_price(product_id)
        if old_price != price:
            PriceDAO.create_product_price(product_id, price)

    @staticmethod
    def create_product_price(product_id: int, price: Decimal):
        """
        Creates product price instance in the db for given product
        It's used during initial product creation
        """
        models.ProductPrice(product_id=product_id, price=price).save()

    @staticmethod
    def get_all_product_price_history(**kwargs) -> QuerySet:
        """
        Returns product price history
        """
        date_start = kwargs.get('date_start')
        aggregation_period = kwargs.get('aggregation_period')
        agg_function = PriceDAO.aggregation_period_dict[aggregation_period]
        return models.ProductPrice.objects.annotate(period=agg_function('date_actual'), avg_price=Avg('price')) \
            .values('product_id', 'period', 'avg_price') \
            .filter(date_actual__gte=date_start)\
            .order_by('period')

    @staticmethod
    def get_product_price_history_by_id(id_list: List[int], **kwargs):
        """
        Returns product price history for particular product
        """
        return PriceDAO.get_all_product_price_history(**kwargs).filter(product_id__in=id_list)
