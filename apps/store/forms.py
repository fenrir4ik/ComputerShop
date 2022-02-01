from django import forms
from django.core.validators import MinValueValidator
from django.forms import formset_factory

from apps.store.models import Product
from utils.form_validators import name_validator


class ImageForm(forms.Form):
    # image = forms.ImageField(label="Изображение товара")
    image = forms.CharField(validators=[name_validator])


ImageFormSet = formset_factory(ImageForm, extra=1, max_num=3)


class AddProductForm(forms.ModelForm):
    price = forms.DecimalField(validators=[MinValueValidator(0.01)], decimal_places=2, max_digits=11)

    class Meta:
        model = Product
        fields = ['name', 'price', 'amount', 'category', 'vendor', 'description']

    def __init__(self, data=None, instance=None, **kwargs):
        super().__init__(data=data, instance=instance, **kwargs)
        self.image_formset = ImageFormSet()

    def is_valid(self):
        return super().is_valid() and self.image_formset.is_valid()

    def save(self, commit=True):
        return self.instance
