from abc import ABC, abstractmethod

from apps.store.models import ProductImage, Product
from computershop.settings import DEFAULT_PRODUCT_IMAGE


class BaseImageManager(ABC):
    @abstractmethod
    def add_product_images(self, product: Product, image_list):
        pass

    @abstractmethod
    def update_product_images(self, product: Product, image_list):
        pass


class ImageManager(BaseImageManager):
    def _create_product_image(self, product: Product, image_form, is_main=False):
        """Creates product image from given form"""

        old_image_instance = image_form.cleaned_data.get('id')
        product_image = image_form.save(commit=False)
        if old_image_instance and old_image_instance.image != product_image.image and \
                old_image_instance.image != DEFAULT_PRODUCT_IMAGE:
            old_image_instance.image.delete()
            old_image_instance.save()
        if image_form.cleaned_data and product_image.image:
            product_image.product = product
            product_image.is_main = is_main
            product_image.save()
            return True
        else:
            return False

    def add_product_images(self, product: Product, image_list):
        """
        Retrieves product instance and image_list which
        is formset and performs create of product images
        """
        main_image_empty = True
        for image_form in image_list:
            if self._create_product_image(product, image_form, main_image_empty):
                main_image_empty = False
        # if during add process image wasn't created, create one default image instance
        if main_image_empty:
            ProductImage(product=product, is_main=True).save()

    def update_product_images(self, product: Product, image_list):
        """
        Retrieves product instance and image_list which
        is formset and performs update of product images
        """
        main_image_empty = True
        num_delete_checkboxes = 0

        for image_form in image_list:
            # check if old image instance exists and should be deleted
            if image_form.cleaned_data.get('DELETE'):
                old_image_instance = image_form.cleaned_data.get('id')
                if old_image_instance:
                    old_image_instance.delete()
                num_delete_checkboxes += 1
            else:
                if self._create_product_image(product, image_form, main_image_empty):
                    main_image_empty = False
        # if during update process image wasn't created, or all
        # images have been deleted create default image instance
        if main_image_empty or num_delete_checkboxes == len(image_list):
            ProductImage(product=product, is_main=True).save()
