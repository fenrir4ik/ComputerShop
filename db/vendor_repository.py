from typing import List

from django.apps import apps
from django.db.models import QuerySet


class VendorRepository:
    def __init__(self):
        self.Vendor = apps.get_model('store', 'Vendor')

    def get_vendors_for_product_category(self, category_list: List[int]) -> QuerySet:
        """Returns vendor list where for any vendor exists product with given category"""
        return self.Vendor.objects.filter(products__category_id__in=category_list).distinct()
