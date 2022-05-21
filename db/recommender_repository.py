from typing import List

from django.apps import apps
from django.db.models import QuerySet, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay

from db.price_repository import PriceRepository
from services.settings import REC_START, REC_PERIOD


class RecommenderRepository:
    __aggregation_period_dict = {
        'month': TruncMonth,
        'week': TruncWeek,
        'day': TruncDay
    }

    def __init__(self):
        self.CartItem = apps.get_model('store', 'CartItem')
        self.OrderStatus = apps.get_model('store', 'OrderStatus')

    def get_price_history(self, *id_list) -> QuerySet:
        return PriceRepository().get_product_price_history_by_id(*id_list,
                                                                 aggregation_period=REC_PERIOD,
                                                                 date_start=REC_START)

    def get_sales_history(self, *id_list) -> QuerySet:
        date_start = REC_START
        aggregation_period = REC_PERIOD
        agg_function = self.__aggregation_period_dict[aggregation_period]
        return self.CartItem.objects.values('product_id') \
            .annotate(period=agg_function('order__date_end'), total_products=Sum('amount')) \
            .values('product_id', 'period', 'total_products') \
            .filter(order__date_end__gte=date_start,
                    product_id__in=id_list,
                    order__status_id=self.OrderStatus.retrieve_id("completed")) \
            .order_by('period')
