from typing import List, Dict

from db.characteristic_repository import CharacteristicRepository


class CharacteristicService:
    """Service for managing product characteristics"""

    def add_product_characteristics(self, product_id: int, characteristics: List[Dict]):
        for characteristic in characteristics:
            name = characteristic.get('Characteristic')
            value = characteristic.get('Value')
            CharacteristicRepository().create_product_characteristic(product_id, name=name, value=value)

    def update_product_characteristics(self, product_id: int, characteristics: List[Dict]):
        CharacteristicRepository().delete_product_characteristics(product_id)
        self.add_product_characteristics(product_id, characteristics)
