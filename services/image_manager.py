from typing import List

from services.constants import PRODUCT_IMAGE_MAX_AMOUNT
from services.dao.image_dao import ImageDao


class ImageManager:
    @staticmethod
    def add_product_images(product_id: int, image_list: List[dict]):
        main_image_empty = True
        for image_dict in image_list:
            if image_dict:
                ImageDao.create_product_image(product_id, image_dict.get('image'), main_image_empty)
                main_image_empty = False
        if main_image_empty:
            ImageDao.create_default_product_image(product_id)

    @staticmethod
    def update_product_images(product_id: int, image_list: List[dict]):
        image_list = _parse_image_formset_to_list(image_list)

        if all(map(lambda image: image.get('delete'), image_list)):
            ImageDao.delete_all_product_images(product_id)
            ImageDao.create_default_product_image(product_id)
            return

        if ImageManager.__images_update_available(product_id, image_list):
            main_image_empty = True
            for image_dict in image_list:
                if image_dict:
                    old_image_id = image_dict.get('old_image_id')
                    delete = image_dict.get('delete')
                    image = image_dict.get('image')

                    if delete and old_image_id:
                        ImageDao.delete_image_by_id(old_image_id)
                    elif old_image_id:
                        if ImageDao.replace_image_by_id(old_image_id, image, main_image_empty):
                            main_image_empty = False
                    elif image and not old_image_id and not delete:
                        ImageDao.create_product_image(product_id, image, main_image_empty)
                        main_image_empty = False
            if main_image_empty:
                ImageDao.create_default_product_image(product_id)

    @staticmethod
    def __images_update_available(product_id: int, image_list: List[dict]) -> bool:
        """Check if can update images to prevent incompatible data during simultaneous product editing"""
        current_image_n = ImageDao.get_product_image_number(product_id)
        created_image_n = 0
        deleted_image_n = 0
        for image_dict in image_list:
            old_image_id = image_dict.get('old_image_id')
            delete = image_dict.get('delete')
            image = image_dict.get('image')

            if delete and old_image_id:
                deleted_image_n += 1
            elif image and not old_image_id and not delete:
                created_image_n += 1
        image_number_after_update = current_image_n - deleted_image_n + created_image_n
        return image_number_after_update <= PRODUCT_IMAGE_MAX_AMOUNT


def _parse_image_formset_to_list(cleaned_data: list) -> List[dict]:
    """
    Retrieves cleaned data and parse it into the list of dicts for future product images updating
    Returns list of dicts with keys image, old_image_id, delete
    """
    image_list = []
    for form in cleaned_data:
        if form:
            image_list.append({
                'image': form.get('image'),
                'old_image_id': form.get('id').id if form.get('id') else None,
                'delete': form.get('DELETE')
            })
        else:
            image_list.append({})
    return image_list
