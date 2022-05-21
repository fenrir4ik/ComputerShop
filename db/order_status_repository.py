from typing import Set

from django.apps import apps
from django.db.models import QuerySet


class OrderStatusRepository:
    def __init__(self):
        self.OrderStatus = apps.get_model('store', 'OrderStatus')

    def get_statuses_by_id_list(self, status_list: Set[int]) -> QuerySet:
        """Returns order statuses those id's are in status_list"""
        return self.OrderStatus.objects.filter(id__in=status_list)
