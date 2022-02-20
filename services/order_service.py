from typing import Set

from django.db.models import QuerySet

from apps.store.models import OrderStatus
from services.dao.order_status_dao import OrderStatusDAO


class OrderService:
    """
    "new": 1,  # Ожидает подтверждения
    "confirmed": 2,  # "Подтвержден"
    "packed_up": 3,  # "Комплектуется"
    "on_way": 4,  # "Следует в город получателя"
    "at_post": 5,  # "Находится в почтовом отделении"
    "completed": 6,  # "Выполнен"
    "canceled": 7,  # "Отменен"
    "not_picked": 8,  # "Получатель не забрал заказ"
    "in_shop": 9,  # "Находится в магазине"

    1 - 2 - 3 - 4 - 5 - 6 # client picked up order from post office
        2 - 3 - 4 - 5 - 8 # client didn't pick up order from post office
        2 - 3 - 9 - 6     # client picked up order from shop
        2 - 3 - 9 - 7     # client didn't pick up order from shop
        2 - 7             # admin canceled the order after its confirmation
        2 - 3 - 7         # admin canceled the order during picking
    """
    __status_pipelines_without_delivery = [["confirmed", "packed_up", "in_shop", "completed"],
                                           ["confirmed", "packed_up", "in_shop", "canceled"]]

    __status_pipelines_with_delivery = [["confirmed", "packed_up", "on_way", "at_post", "completed"],
                                        ["confirmed", "packed_up", "on_way", "at_post", "not_picked"]]

    __status_pipelines_for_new_order = [["new", "confirmed", "canceled"]]

    def __init__(self, status_id: int, delivery_available: bool):
        self.current_status_id = status_id
        self.delivery_available = delivery_available

        if self.current_status_id == OrderStatus.retrieve_id('new'):
            self.__status_pipelines = self.__status_pipelines_for_new_order
        else:
            if delivery_available:
                self.__status_pipelines = self.__status_pipelines_with_delivery
            else:
                self.__status_pipelines = self.__status_pipelines_without_delivery

    def __get_future_statuses_id_list(self) -> Set[int]:
        future_statuses = []
        for pipeline in self.__status_pipelines:
            pipeline = [OrderStatus.retrieve_id(status) for status in pipeline]
            if self.current_status_id in pipeline:
                future_statuses.extend(pipeline[pipeline.index(self.current_status_id):])
        return set(future_statuses)

    def get_future_statuses(self) -> QuerySet:
        id_list = self.__get_future_statuses_id_list()
        return OrderStatusDAO.get_statuses_by_id_list(id_list)