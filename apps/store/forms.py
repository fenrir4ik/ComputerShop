from django import forms
from django.core.validators import MinValueValidator

from apps.store.models import Product


class AddProductForm(forms.ModelForm):
    price = forms.DecimalField(validators=[MinValueValidator('0.01')], decimal_places=2, max_digits=11)
    # images = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'price', 'amount', 'category', 'vendor', 'description']
