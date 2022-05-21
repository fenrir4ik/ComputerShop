from decimal import Decimal
from typing import List

from django.apps import apps
from django.db.models import Avg, QuerySet
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay


class PriceRepository:
    aggregation_period_dict = {
        'month': TruncMonth,
        'week': TruncWeek,
        'day': TruncDay
    }

    def __init__(self):
        self.ProductPrice = apps.get_model('store', 'ProductPrice')

    def get_last_product_price(self, product_id: int):
        return self.ProductPrice.objects.filter(product_id=product_id) \
            .values_list('price', flat=True).order_by('-date_actual')[0]

    def update_product_price(self, product_id: int, price: Decimal):
        """
        Updates price of given product
        This method is used during product update
        Product price history will be formed as a result of multiple price updates
        """
        old_price = self.get_last_product_price(product_id)
        if old_price != price:
            self.create_product_price(product_id, price)

    def create_product_price(self, product_id: int, price: Decimal):
        """
        Creates product price instance in the db for given product
        It's used during initial product creation
        """
        self.ProductPrice(product_id=product_id, price=price).save()

    def get_all_products_price_history(self, date_start, aggregation_period) -> QuerySet:
        """
        Returns product price history
        """
        agg_function = self.aggregation_period_dict[aggregation_period]
        return self.ProductPrice.objects.annotate(period=agg_function('date_actual'), avg_price=Avg('price')) \
            .values('product_id', 'period', 'avg_price') \
            .filter(date_actual__gte=date_start) \
            .order_by('period')

    def get_product_price_history_by_id(self, id_list: List[int], date_start, aggregation_period):
        """
        Returns product price history for particular product or set of products
        """
        return self.get_all_products_price_history(date_start, aggregation_period).filter(product_id__in=id_list)
