from typing import List

from django.db.models import QuerySet, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay

import apps.store.models as models
from db.price_dao import PriceDAO
from services.constants import REC_START, REC_PERIOD


class RecommenderDAO:
    aggregation_period_dict = {
        'month': TruncMonth,
        'week': TruncWeek,
        'day': TruncDay
    }

    @staticmethod
    def get_cart_products_id(cart_id: int) -> QuerySet:
        return models.CartItem.objects.filter(order_id=cart_id).values_list('product_id', flat=True)

    @staticmethod
    def get_price_history(id_list: List[int]) -> QuerySet:
        return PriceDAO.get_product_price_history_by_id(id_list,
                                                        aggregation_period=REC_PERIOD,
                                                        date_start=REC_START)

    @staticmethod
    def get_sales_history(id_list: List[int]) -> QuerySet:
        date_start = REC_START
        aggregation_period = REC_PERIOD
        agg_function = PriceDAO.aggregation_period_dict[aggregation_period]
        return models.CartItem.objects.values('product_id').annotate(period=agg_function('order__date_end'), total_products=Sum('amount')) \
            .values('product_id', 'period', 'total_products') \
            .filter(order__date_end__gte=date_start,
                    product_id__in=id_list,
                    order__status_id=models.OrderStatus.retrieve_id("completed"))\
            .order_by('period')
