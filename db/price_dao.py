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
    def update_product_price(product_id: int, price: Decimal):
        """
        Updates price of given product
        This method is used during product update
        Product price history will be formed as a result of multiple price updates
        """
        old_price_instance = models.ProductPrice.objects.filter(product_id=product_id).order_by('-date_actual').first()
        if old_price_instance.price != price:
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
        return models.ProductPrice.objects.annotate(period=agg_function('date_actual')) \
            .values('product_id', 'period') \
            .annotate(avg_price=Avg('price')) \
            .filter(date_actual__gte=date_start)

    @staticmethod
    def get_product_price_history_by_id(product_ids: List[int], **kwargs):
        """
        Returns product price history for particular product
        """
        return PriceDAO.get_all_product_price_history(**kwargs).filter(product_id__in=product_ids)