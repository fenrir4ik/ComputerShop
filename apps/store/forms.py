from django import forms
from django.utils import timezone

from apps.store.models import Order, OrderStatus
from apps.user.forms import UserBaseForm
from db.order_dao import OrderDAO


class AddProductToCartForm(forms.Form):
    """Form is used for adding products to shopping cart"""

    def __init__(self, amount_in_cart, max_amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        amount_in_cart = None if amount_in_cart < 1 else amount_in_cart
        self.fields['amount'] = forms.IntegerField(label="Кол-во",
                                                   min_value=1,
                                                   max_value=max_amount,
                                                   initial=amount_in_cart)


class CreateOrderForm(UserBaseForm, forms.ModelForm):
    """Form is used for order creation"""

    class Meta:
        model = Order
        fields = ['name', 'surname', 'patronymic', 'phone_number', 'email', 'address', 'payment']

    address = forms.CharField(
        label="Адрес доставки",
        widget=forms.TextInput(attrs={'placeholder': 'Адрес доставки'}),
        required=False,
        empty_value=None,
    )

    def __init__(self, user, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'required': True})
        self.fields['payment'].widget.attrs.update({'required': True})

        self.user = user

        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        cart_id = OrderDAO.get_user_cart_id(self.user.pk)
        order = super().save(commit=False)
        order.pk = cart_id
        order.user = self.user
        order.status_id = OrderStatus.retrieve_id('new')
        order.date_start = timezone.now()
        order.save()
        return order
