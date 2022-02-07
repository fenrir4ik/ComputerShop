from typing import List

from apps.store.models import Product
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
