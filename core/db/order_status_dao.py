from typing import Set

from django.db.models import QuerySet

from apps.store.models import OrderStatus


class OrderStatusDAO:
    @staticmethod
    def get_statuses_by_id_list(status_list: Set[int]) -> QuerySet:
        return OrderStatus.objects.filter(id__in=status_list)
