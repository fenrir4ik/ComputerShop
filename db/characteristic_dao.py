from typing import Dict, List

from django.db.models import F

import apps.store.models as models


class CharacteristicDAO:
    """DAO is used to interact with ProductImage model instances"""

    @staticmethod
    def create_product_characteristic(product_id: int, name: str, value: str):
        """Saves single product characteristic with name and value"""
        char, _ = models.Characteristic.objects.get_or_create(name=name)
        models.ProductCharacteristic(product_id=product_id, characteristic=char, value=value).save()

    @staticmethod
    def delete_product_characteristics(product_id: int):
        """Deletes all characteristics of given product"""
        models.ProductCharacteristic.objects.filter(product_id=product_id).delete()
        models.Characteristic.objects.filter(products=None).delete()

    @staticmethod
    def get_product_characteristics(product_id: int) -> List[Dict]:
        return models.ProductCharacteristic.objects.filter(product_id=product_id) \
            .select_related('characteristic') \
            .values('value', name=F('characteristic__name'))
