from django.db.models import OuterRef, Subquery, Q

from apps.store.models import Product, ProductPrice, ProductImage
from computershop.settings import DEFAULT_PRODUCT_IMAGE


class BaseProductService:
    def __init__(self, instance=None):
        if instance is None:
            raise ValueError("Missing instance in constructor")
        elif not isinstance(instance, Product):
            raise ValueError(f"Instance should be of type {Product}, but type {type(instance)} given")
        self.product = instance


class ProductRetrieveService:
    def get_products_list(self, include_price=True, include_image=True):
        products = Product.objects.select_related('vendor', 'category')
        if include_price:
            actual_price = ProductPrice.objects.filter(product=OuterRef('pk')).order_by('-date_actual')
            products = products.annotate(price=Subquery(actual_price.values('price')[:1]))
        if include_image:
            product_image = ProductImage.objects.filter(Q(product=OuterRef('pk')) & Q(is_main=True))
            products = products.annotate(image=Subquery(product_image.values('image')[:1]))
        return products


class ProductDestroyService(BaseProductService):
    def delete_product(self):
        self.product.delete()


class PriceService(BaseProductService):
    def save_product_price(self, price):
        old_price_instance = ProductPrice.objects.filter(product=self.product).order_by('-date_actual').first()
        if old_price_instance and old_price_instance.price != price or not old_price_instance:
            ProductPrice(product=self.product, price=price).save()


# Переделать без форм
class ImageService(BaseProductService):
    def _create_product_image(self, image_form, is_main=False):
        """Creates product image from given form"""

        old_image_instance = image_form.cleaned_data.get('id')
        product_image = image_form.save(commit=False)
        if old_image_instance and old_image_instance.image != product_image.image and \
                old_image_instance.image != DEFAULT_PRODUCT_IMAGE:
            old_image_instance.image.delete()
            old_image_instance.save()
        if image_form.cleaned_data and product_image.image:
            product_image.product = self.product
            product_image.is_main = is_main
            product_image.save()
            return True
        else:
            return False

    def add_product_images(self, image_list):
        """
        Retrieves product instance and image_list which
        is formset and performs create of product images
        """
        main_image_empty = True
        for image_form in image_list:
            if self._create_product_image(image_form, main_image_empty):
                main_image_empty = False
        # if during add process image wasn't created, create one default image instance
        if main_image_empty:
            ProductImage(product=self.product, is_main=True).save()

    def update_product_images(self, image_list):
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
                if self._create_product_image(image_form, main_image_empty):
                    main_image_empty = False
        # if during update process image wasn't created, or all
        # images have been deleted create default image instance
        if main_image_empty or num_delete_checkboxes == len(image_list):
            ProductImage(product=self.product, is_main=True).save()


class ProductService(BaseProductService):
    product_price_manager = PriceService
    image_manager = ImageService

    def add_additional_data(self, price, image_list):
        self.product_price_manager(self.product).save_product_price(price)
        self.image_manager(self.product).add_product_images(image_list)

    def update_additional_data(self, price, image_list):
        self.product_price_manager(self.product).save_product_price(price)
        self.image_manager(self.product).update_product_images(image_list)
