from typing import Dict, List

from django.db.models import F

from apps.store.models import Characteristic, ProductCharacteristic


class CharacteristicDAO:
    """DAO is used to interact with ProductImage model instances"""

    @staticmethod
    def create_product_characteristic(product_id: int, name: str, value: str):
        """Saves single product characteristic with name and value"""
        char, _ = Characteristic.objects.get_or_create(name=name)
        ProductCharacteristic(product_id=product_id, characteristic=char, value=value).save()

    @staticmethod
    def delete_product_characteristics(product_id: int):
        """Deletes all characteristics of given product"""
        ProductCharacteristic.objects.filter(product_id=product_id).delete()
        Characteristic.objects.filter(products=None).delete()

    @staticmethod
    def get_product_characteristics(product_id: int) -> List[Dict]:
        return ProductCharacteristic.objects.filter(product_id=product_id) \
            .select_related('characteristic') \
            .values('value', name=F('characteristic__name'))
