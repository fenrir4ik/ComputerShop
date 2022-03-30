from typing import List, Dict

from db.characteristic_dao import CharacteristicDAO


class CharacteristicService:
    """Service for managing product characteristics"""

    @staticmethod
    def add_product_characteristics(product_id: int, characteristics: List[Dict]):
        for characteristic in characteristics:
            name = characteristic.get('Characteristic')
            value = characteristic.get('Value')
            CharacteristicDAO.create_product_characteristic(product_id, name=name, value=value)

    @staticmethod
    def update_product_characteristics(product_id: int, characteristics: List[Dict]):
        CharacteristicDAO.delete_product_characteristics(product_id)
        CharacteristicService.add_product_characteristics(product_id, characteristics)
