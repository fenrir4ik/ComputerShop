from decimal import Decimal

from django.db.models import Avg, QuerySet
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.store.models import ProductPrice


class PriceDAO:
    """DAO is used to interact with ProductPrice model instances"""

    @staticmethod
    def update_product_price(product_id: int, price: Decimal):
        """
        Updates price of given product
        This method is used during product update
        Product price history will be formed as a result of multiple price updates
        """
        old_price_instance = ProductPrice.objects.filter(product_id=product_id).order_by('-date_actual').first()
        if old_price_instance.price != price:
            PriceDAO.create_product_price(product_id, price)

    @staticmethod
    def create_product_price(product_id: int, price: Decimal):
        """
        Creates product price instance in the db for given product
        It's used during initial product creation
        """
        ProductPrice(product_id=product_id, price=price).save()

    @staticmethod
    def get_product_price_history(product_id: int) -> QuerySet:
        """
        Returns yearly product price history
        """
        year_ago_date = timezone.now() - timezone.timedelta(days=365)
        return ProductPrice.objects.annotate(month=TruncMonth('date_actual')) \
            .values('month') \
            .annotate(avg_price=Avg('price')) \
            .filter(product_id=product_id, date_actual__gte=year_ago_date)
