from django import forms
from django.core.validators import MinValueValidator
from django.forms import formset_factory

from apps.store.models import Product


class ImageForm(forms.Form):
    image = forms.ImageField(label="Изображение товара", required=False)


ImageFormSet = formset_factory(ImageForm, extra=1, max_num=3)


class AddProductForm(forms.ModelForm):
    price = forms.DecimalField(validators=[MinValueValidator(0.01)], decimal_places=2, max_digits=11)

    class Meta:
        model = Product
        fields = ['name', 'price', 'amount', 'category', 'vendor', 'description']

    def __init__(self, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.image_formset = ImageFormSet(data=data, files=files)

    def is_valid(self):
        return self.image_formset.is_valid() and super().is_valid()

    def save(self, commit=True):
        print(self.cleaned_data)
        for item in self.image_formset:
            if item.cleaned_data:
                print(item.cleaned_data)
        return self.instance
# think about only images check