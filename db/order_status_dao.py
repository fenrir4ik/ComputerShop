from typing import Set

from django.db.models import QuerySet

from apps.store.models import OrderStatus


class OrderStatusDAO:
    """DAO is used to interact with OrderStatus model instances"""

    @staticmethod
    def get_statuses_by_id_list(status_list: Set[int]) -> QuerySet:
        """Returns order statuses those id's are in status_list"""
        return OrderStatus.objects.filter(id__in=status_list)
