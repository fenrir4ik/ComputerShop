from django.db.models import QuerySet

from apps.store.models import Review


class ReviewDAO:
    """DAO is used to interact with Vendor model instances"""

    @staticmethod
    def get_product_reviews(product_id: int) -> QuerySet:
        return Review.objects.prefetch_related('user')\
            .only('user_id', 'product_id', 'message')\
            .filter(product_id=product_id)
