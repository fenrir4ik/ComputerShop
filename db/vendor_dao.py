from typing import List

from django.db.models import QuerySet

from apps.store.models import Vendor


class VendorDAO:
    @staticmethod
    def get_vendors_for_product_category(category_list: List[int]) -> QuerySet:
        return Vendor.objects.filter(products__category_id__in=category_list).distinct()
