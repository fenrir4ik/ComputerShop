from typing import List

from db.image_dao import ImageDAO
from services.constants import PRODUCT_IMAGE_MAX_AMOUNT


def _parse_image_formset_to_list(cleaned_data: list) -> List[dict]:
    """
    Retrieves cleaned data and parse it into the list of dicts for future product images updating
    Returns list of dicts with keys: image, old_image_id, delete
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


class ImageService:
    """Service is used for product image managing, like adding and updating product images"""
    @staticmethod
    def add_product_images(product_id: int, image_list: List[dict]):
        """Method takes in product id and image list and adds images for given product"""
        main_image_empty = True
        for image_dict in image_list:
            if image_dict:
                ImageDAO.create_product_image(product_id, image_dict.get('image'), main_image_empty)
                main_image_empty = False
        if main_image_empty:
            ImageDAO.create_default_product_image(product_id)

    @staticmethod
    def update_product_images(product_id: int, image_list: List[dict]):
        """Method takes in product id and image list and updates images for given product"""
        image_list = _parse_image_formset_to_list(image_list)

        if all(map(lambda image: image.get('delete'), image_list)):
            ImageDAO.delete_all_product_images(product_id)
            ImageDAO.create_default_product_image(product_id)
            return

        if ImageService.__images_update_available(product_id, image_list):
            main_image_empty = True
            for image_dict in image_list:
                if image_dict:
                    old_image_id = image_dict.get('old_image_id')
                    delete = image_dict.get('delete')
                    image = image_dict.get('image')

                    if delete and old_image_id:
                        ImageDAO.delete_image_by_id(old_image_id)
                    elif old_image_id:
                        if ImageDAO.replace_image_by_id(old_image_id, image, main_image_empty):
                            main_image_empty = False
                    elif image and not old_image_id and not delete:
                        ImageDAO.create_product_image(product_id, image, main_image_empty)
                        main_image_empty = False
            if main_image_empty:
                ImageDAO.create_default_product_image(product_id)

    @staticmethod
    def __images_update_available(product_id: int, image_list: List[dict]) -> bool:
        """Check if image update available to prevent incompatible data creation during simultaneous product editing"""
        current_image_n = ImageDAO.get_product_image_number(product_id)
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
