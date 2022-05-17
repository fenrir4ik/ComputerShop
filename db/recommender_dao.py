from typing import List

from django.db.models import QuerySet

import apps.store.models as models
from db.price_dao import PriceDAO
from services.constants import REC_T_START, REC_PERIOD


class RecommenderDAO:
    @staticmethod
    def get_cart_products_id(cart_id: int) -> QuerySet:
        return models.CartItem.objects.filter(order_id=cart_id).values_list('product_id', flat=True)

    @staticmethod
    def get_price_history(product_id_list: List[int]) -> QuerySet:
        return PriceDAO.get_product_price_history_by_id(product_ids=product_id_list,
                                                        aggregation_period=REC_PERIOD,
                                                        date_start=REC_T_START)

    @staticmethod
    def get_sales_history(product_id_list: List[int]) -> QuerySet:
        return None
