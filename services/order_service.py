from apps.store.models import Order
from services.base_service import BaseService


class BaseProductService(BaseService):
    instance_class = Order
