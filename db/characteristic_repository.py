from typing import Dict, List

from django.apps import apps
from django.db.models import F


class CharacteristicRepository:
    def __init__(self):
        self.ProductCharacteristic = apps.get_model('store', 'ProductCharacteristic')
        self.Characteristic = apps.get_model('store', 'Characteristic')

    def create_product_characteristic(self, product_id: int, name: str, value: str):
        """Saves single product characteristic with name and value"""
        char, _ = self.Characteristic.objects.get_or_create(name=name)
        self.ProductCharacteristic(product_id=product_id, characteristic=char, value=value).save()

    def delete_product_characteristics(self, product_id: int):
        """Deletes all characteristics of given product"""
        self.ProductCharacteristic.objects.filter(product_id=product_id).delete()
        self.Characteristic.objects.filter(products=None).delete()

    def get_product_characteristics(self, product_id: int) -> List[Dict]:
        return self.ProductCharacteristic.objects.filter(product_id=product_id) \
            .select_related('characteristic') \
            .values('value', name=F('characteristic__name'))
