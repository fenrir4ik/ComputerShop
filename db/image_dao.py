from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile

from apps.store.models import ProductImage
from services.constants import DEFAULT_PRODUCT_IMAGE


class ImageDAO:
    """DAO is used to interact with ProductImage model instances"""

    @staticmethod
    def create_product_image(product_id: int,
                             image: Union[ImageFieldFile, InMemoryUploadedFile],
                             is_main: bool = False):
        """Creates product image instance in the db with given attributes"""
        ProductImage(product_id=product_id, is_main=is_main, image=image).save()

    @staticmethod
    def create_default_product_image(product_id: int):
        """Creates product image instance in the db with given attributes, but default image"""
        ProductImage(product_id=product_id, is_main=True).save()

    @staticmethod
    def delete_all_product_images(product_id: int):
        """Deletes all product images of product with given id"""
        ProductImage.objects.filter(product_id=product_id).delete()

    @staticmethod
    def delete_image_by_id(id: int):
        """Deletes product instance using given id"""
        ProductImage.objects.filter(pk=id).delete()

    @staticmethod
    def replace_image_by_id(id: int, image: Union[ImageFieldFile, InMemoryUploadedFile], is_main: bool) -> bool:
        """Replaces product instance image with new image"""
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
        """Returns product image amount of particular product"""
        return ImageDAO.get_product_images(product_id).count()

    @staticmethod
    def get_product_images(product_id: int) -> QuerySet:
        """Returns product images of particular product"""
        return ProductImage.objects.filter(product_id=product_id)
