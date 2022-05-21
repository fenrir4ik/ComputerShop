from django.apps import apps
from django.db.models import QuerySet


class ReviewRepository:
    def __init__(self):
        self.Review = apps.get_model('store', 'Review')

    def get_product_reviews(self, product_id: int) -> QuerySet:
        return self.Review.objects.prefetch_related('user') \
            .only('user_id', 'product_id', 'message') \
            .filter(product_id=product_id)
