from typing import Union

from django.apps import apps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile

from services.settings import DEFAULT_PRODUCT_IMAGE


class ImageRepository:
    def __init__(self):
        self.ProductImage = apps.get_model('store', 'ProductImage')

    def create_product_image(self,
                             product_id: int,
                             image: Union[ImageFieldFile, InMemoryUploadedFile],
                             is_main: bool = False):
        """Creates product image instance in the db with given attributes"""
        self.ProductImage(product_id=product_id, is_main=is_main, image=image).save()

    def create_default_product_image(self, product_id: int):
        """Creates product image instance in the db with given attributes, but default image"""
        self.ProductImage(product_id=product_id, is_main=True).save()

    def delete_all_product_images(self, product_id: int):
        """Deletes all product images of product with given id"""
        self.ProductImage.objects.filter(product_id=product_id).delete()

    def delete_image_by_id(self, image_id: int):
        """Deletes product instance using given id"""
        self.ProductImage.objects.filter(pk=image_id).delete()

    def replace_image_by_id(self,
                            image_id: int,
                            image: Union[ImageFieldFile, InMemoryUploadedFile],
                            is_main: bool) -> bool:
        """Replaces product instance image with new image"""
        try:
            image_instance = self.ProductImage.objects.get(pk=image_id)
            if image_instance.image != image and image_instance.image != DEFAULT_PRODUCT_IMAGE:
                image_instance.image.delete()
            image_instance.image = image
            image_instance.is_main = is_main
            image_instance.save()
            return True
        except self.ProductImage.DoesNotExist:
            return False

    def get_product_image_number(self, product_id: int) -> int:
        """Returns product image amount of particular product"""
        return self.get_product_images(product_id).count()

    def get_product_images(self, product_id: int) -> QuerySet:
        """Returns product images of particular product"""
        return self.ProductImage.objects.filter(product_id=product_id)
