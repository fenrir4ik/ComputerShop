from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile

from apps.store.models import ProductImage
from services.constants import DEFAULT_PRODUCT_IMAGE


class ImageDao:
    @staticmethod
    def create_product_image(product_id: int,
                             image: Union[ImageFieldFile, InMemoryUploadedFile],
                             is_main: bool = False):
        ProductImage(product_id=product_id, is_main=is_main, image=image).save()

    @staticmethod
    def create_default_product_image(product_id: int):
        ProductImage(product_id=product_id, is_main=True).save()

    @staticmethod
    def delete_all_product_images(product_id: int):
        ProductImage.objects.filter(product_id=product_id).delete()

    @staticmethod
    def delete_image_by_id(id: int):
        ProductImage.objects.filter(pk=id).delete()

    @staticmethod
    def replace_image_by_id(id: int, image: Union[ImageFieldFile, InMemoryUploadedFile], is_main: bool) -> bool:
        try:
            image_instance = ProductImage.objects.get(pk=id)
            if image_instance.image != image and image_instance.image != DEFAULT_PRODUCT_IMAGE:
                image_instance.image.delete()
            image_instance.image = image
            image_instance.is_main = is_main
            image_instance.save()
            return True
        except ProductImage.DoesNotExist:
            return False

    @staticmethod
    def get_product_image_number(product_id: int) -> int:
        return ImageDao.get_product_images(product_id).count()

    @staticmethod
    def get_product_images(product_id: int) -> QuerySet:
        return ProductImage.objects.filter(product_id=product_id)
