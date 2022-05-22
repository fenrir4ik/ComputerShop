from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import QuerySet, Sum, Max, F
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
        self.Product = apps.get_model('store', 'Product')
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

    def get_products_last_bought_time(self) -> QuerySet:
        return self.Product.objects.exclude(rating=0.0) \
            .values('id', 'rating') \
            .annotate(last_time=Max('cartitem__order__date_end')) \
            .filter(cartitem__order__date_end__gt=REC_START - relativedelta(weeks=1))

    def decrease_product_rating(self, product_id: int, fading_coefficient: float):
        self.Product.objects.filter(pk=product_id).update(rating=F('rating') * fading_coefficient)
