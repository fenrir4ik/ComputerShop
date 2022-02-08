from typing import List


from apps.store.models import Product
from computershop.settings import PRODUCT_IMAGE_MAX_NUMBER
from services.dao.image_dao import ImageDao


class ImageManager:
    @staticmethod
    def add_product_images(product: Product, image_list: List[dict]):
        main_image_empty = True
        for image_dict in image_list:
            if image_dict:
                ImageDao.create_product_image(product, image_dict.get('image'), main_image_empty)
                main_image_empty = False
        if main_image_empty:
            ImageDao.create_default_product_image(product)

    @staticmethod
    def update_product_images(product: Product, image_list: List[dict]):
        if all(map(lambda image: image.get('delete'), image_list)):
            ImageDao.delete_all_product_images(product)
            ImageDao.create_default_product_image(product)
            return

        if ImageManager._images_update_available(product, image_list):
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
                        ImageDao.create_product_image(product, image, main_image_empty)
                        main_image_empty = False
            if main_image_empty:
                ImageDao.create_default_product_image(product)

    @staticmethod
    def _images_update_available(product: Product, image_list: List[dict]) -> bool:
        """Check if can update images to prevent incompatible data during simultaneous product editing"""
        current_image_n = ImageDao.get_product_image_number(product)
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
        return image_number_after_update <= PRODUCT_IMAGE_MAX_NUMBER