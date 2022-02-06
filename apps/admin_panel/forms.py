from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import formset_factory, inlineformset_factory, BaseInlineFormSet

from apps.store.models import Product, ProductImage
from services.product_service import ProductDataManager
from utils.form_validators import square_image_validator


class ImageForm(forms.ModelForm):
    """
    Form is used in ImageFormSets to add multiple images to the product
    """
    image = forms.ImageField(required=False, validators=[square_image_validator])

    class Meta:
        model = ProductImage
        fields = ['image']

    # CSS REPLACE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'


# FormSet for product images with maximum amount of 3
ImageFormSet = formset_factory(ImageForm, extra=1, max_num=3)


class ProductAddForm(forms.ModelForm):
    """
    Form is used for product creation
    """
    price = forms.DecimalField(validators=[MinValueValidator(0.00)], decimal_places=2, max_digits=11, min_value=0.00)

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
        product_data_manager = ProductDataManager(product)
        product_data_manager.add_additional_data(self.cleaned_data.get('price'), self.image_formset)
        return product


class ProductImageUpdateInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        some_form_is_invalid = False
        for form in self.forms:
            # validate image if it has changed and delete checkbox is not True
            if 'image' in form.changed_data and 'delete' not in form.changed_data:
                try:
                    square_image_validator(form.cleaned_data.get('image'))
                except ValidationError as ex:
                    form.add_error('image', ex.message)
                    some_form_is_invalid = True
        # if some form has changed make form.instance as pk
        # (prevent form.image and other data disappearing)
        if some_form_is_invalid:
            for form in self.forms:
                form.instance = form.cleaned_data.get('id')


# FormSet for updating product images
ProductImageUpdateFormSet = inlineformset_factory(Product,
                                                  ProductImage,
                                                  formset=ProductImageUpdateInlineFormSet,
                                                  fields=['image'],
                                                  can_delete=True,
                                                  max_num=3,
                                                  min_num=1)


class ProductUpdateForm(ProductAddForm):
    def __init__(self, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.image_formset = ProductImageUpdateFormSet(data=data, files=files, instance=instance, **kwargs)
        self.fields['price'].initial = instance.price
