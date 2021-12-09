import requests
from django import forms
from django.core.validators import RegexValidator


class SearchForm(forms.Form):
    search_request = forms.CharField(required=False)


class ProductAmountForm(forms.Form):
    product_amount = forms.IntegerField(required=False)


class CheckoutForm(forms.Form):
    to_name = forms.CharField(max_length=30, required=True,
                                    validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁёІіЇїЄє]{1,30}$',
                                                'Имя должно состоять из букв латиницы или кириллицы')])
    to_surname = forms.CharField(max_length=30, required=True,
                                       validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁёІіЇїЄє]{1,30}$',
                                                   'Фамилия должна состоять из букв латиницы или кириллицы')])
    to_email = forms.EmailField(required=True)
    to_telno = forms.CharField(max_length=12, required=True, validators=[
        RegexValidator(r'^380[0-9]{9}$', 'Номер телефона должен быть длинной в 12 символов и начинаться с 380')])
    address = forms.CharField(max_length=255, required=True)
    payment_type = forms.ChoiceField(choices = [])
