from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator


class ProductForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=True)
    product_price = forms.DecimalField(decimal_places=2, max_digits=9, required=True,
                                       validators=[MinValueValidator(Decimal('0.0'), 'Цена должна быть не отрицательной')])
    product_amount = forms.IntegerField(validators=[MinValueValidator(0, 'Количество товара должно быть не отрицательным')])
    product_description = forms.CharField(error_messages={'required': 'Описание должно быть заполнено'})
    product_image = forms.ImageField(required=False)
    product_type = forms.ChoiceField(choices=[])
    product_vendor = forms.ChoiceField(choices=[])
