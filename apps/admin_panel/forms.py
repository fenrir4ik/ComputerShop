from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import formset_factory, inlineformset_factory, BaseInlineFormSet

from apps.store.models import Product, ProductImage, Order
from services.constants import PRODUCT_IMAGE_MAX_AMOUNT
from services.order_service import OrderService
from services.product_service import AdditionalProductDataService
from utils.form_validators import square_image_validator


class ImageForm(forms.ModelForm):
    """Form is used in ImageFormSets to add multiple images to the product"""
    image = forms.ImageField(required=False, validators=[square_image_validator])

    class Meta:
        model = ProductImage
        fields = ['image']

    # CSS REPLACE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'


class ProductImageUpdateInlineFormSet(BaseInlineFormSet):
    """Formset is used for product image updating"""

    def clean(self):
        super().clean()
        for form in self.forms:
            # validate image if it has changed and delete checkbox is not True
            if 'image' in form.changed_data and 'delete' not in form.changed_data:
                try:
                    square_image_validator(form.cleaned_data.get('image'))
                except ValidationError as ex:
                    form.add_error('image', ex.message)

        # if some form has changed make form.instance as pk
        # (prevent form.image and other data disappearing)
        if self.total_error_count():
            for form in self.forms:
                form.instance = form.cleaned_data.get('id')


# FormSet for product images with maximum amount of PRODUCT_IMAGE_MAX_NUMBER
ImageFormSet = formset_factory(ImageForm, extra=1, max_num=PRODUCT_IMAGE_MAX_AMOUNT)

# FormSet for updating product images
ProductImageUpdateFormSet = inlineformset_factory(Product,
                                                  ProductImage,
                                                  formset=ProductImageUpdateInlineFormSet,
                                                  fields=['image'],
                                                  can_delete=True,
                                                  max_num=PRODUCT_IMAGE_MAX_AMOUNT,
                                                  min_num=1)


class ProductAddForm(forms.ModelForm):
    """Form is used to add new products in admin-panel"""
    price = forms.DecimalField(label="Цена", validators=[MinValueValidator(0.00)], decimal_places=2, max_digits=11,
                               min_value=0.00)

    class Meta:
        model = Product
        fields = ['name', 'price', 'amount', 'category', 'vendor', 'description']

    def __init__(self, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.image_formset = ImageFormSet(data=data, files=files)

        # CSS REPLACE
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return self.image_formset.is_valid() and super().is_valid()

    def save(self, commit=True):
        product = super().save(commit=commit)
        self.save_additional_product_data(product)
        return product

    def save_additional_product_data(self, product):
        if type(self) != ProductAddForm:
            raise NotImplementedError("Implement save_additional_product_data(self, product) method")
        service = AdditionalProductDataService()
        service.add_additional_data(product.pk, self.cleaned_data.get('price'), self.image_formset.cleaned_data)


class ProductUpdateForm(ProductAddForm):
    """Form is used to update products in admin-panel"""

    def __init__(self, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.image_formset = ProductImageUpdateFormSet(data=data, files=files, instance=instance, **kwargs)
        self.fields['price'].initial = instance.price

    def save(self, commit=True):
        product = super().save(commit=commit)
        return product

    def save_additional_product_data(self, product):
        service = AdditionalProductDataService()
        service.update_additional_data(product.pk, self.cleaned_data.get('price'), self.image_formset.cleaned_data)


class OrderChangeForm(forms.ModelForm):
    """Form is used to update user order information and status"""

    class Meta:
        model = Order
        fields = ['name', 'surname', 'patronymic', 'email', 'phone_number', 'address', 'date_start', 'date_end',
                  'payment', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

        self.fields['address'].empty_value = None

        service = OrderService(status_id=self.instance.status_id, delivery_available=bool(self.instance.address))
        self.fields['status'].queryset = service.get_future_statuses()

        readonly_fields = ['date_start', 'date_end']
        if not self.instance.is_new:
            readonly_fields.extend(['name', 'surname', 'patronymic', 'email', 'phone_number', 'address', 'payment'])
        for field in readonly_fields:
            self.fields[field].disabled = True
