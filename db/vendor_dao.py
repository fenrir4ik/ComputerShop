from typing import List

from django.db.models import QuerySet

from apps.store.models import Vendor


class VendorDAO:
    """DAO is used to interact with Vendor model instances"""

    @staticmethod
    def get_vendors_for_product_category(category_list: List[int]) -> QuerySet:
        """Returns vendor list where for any vendor exists product with given category"""
        return Vendor.objects.filter(products__category_id__in=category_list).distinct()
