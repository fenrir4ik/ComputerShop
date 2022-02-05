from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import MinValueValidator
from django.forms import formset_factory

from apps.store.models import Product, ProductImage, ProductPrice


class ImageForm(forms.ModelForm):
    """
    Form is used in ImageFormSets to add multiple images to the product
    """
    class Meta:
        model = ProductImage
        fields = ['image']

    # CSS REPLACE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        width, height = get_image_dimensions(image)
        if width == height:
            return image
        else:
            raise ValidationError("Изображение должно быть квадратным")


# FormSet for product images with maximum amount of 3
ImageFormSet = formset_factory(ImageForm, extra=1, max_num=3)


class AddProductForm(forms.ModelForm):
    """
    Form is used for product creation
    """
    price = forms.DecimalField(validators=[MinValueValidator(0.01)], decimal_places=2, max_digits=11)

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
        ProductPrice(product=product, price=self.cleaned_data.get('price')).save()
        is_main_image = True
        for image_form in self.image_formset:
            if image_form.cleaned_data:
                product_image = image_form.save(commit=False)
                product_image.product = product
                product_image.is_main = is_main_image
                product_image.save()
                is_main_image = False
        if is_main_image:
            ProductImage(product=product, is_main=is_main_image).save()
        return product
