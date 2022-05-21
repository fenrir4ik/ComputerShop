from django import forms
from django.utils import timezone

from apps.store.models import Order, OrderStatus
from apps.user.forms import UserBaseForm
from db.cart_item_repository import CartItemRepository
from db.order_repository import OrderRepository


class AddProductToCartForm(forms.Form):
    """Form is used for adding products to shopping cart"""

    def __init__(self, amount_in_cart, max_amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        amount_in_cart = None if amount_in_cart < 1 else amount_in_cart
        self.fields['amount'] = forms.IntegerField(label="В корзине",
                                                   min_value=1,
                                                   max_value=max_amount,
                                                   initial=amount_in_cart)


class CreateOrderForm(UserBaseForm, forms.ModelForm):
    """Form is used for order creation"""

    class Meta:
        model = Order
        fields = ['name', 'surname', 'patronymic', 'phone_number', 'email', 'address', 'payment']

    def __init__(self, user, data=None, files=None, instance=None, **kwargs):
        super().__init__(data=data, files=files, instance=instance, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'required': True})
        self.fields['payment'].widget.attrs.update({'required': True})
        self.fields['address'].empty_value = None

        self.user = user

        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        cart_id = OrderRepository().get_user_cart_id(self.user.pk)
        order = super().save(commit=False)
        order.pk = cart_id
        order.user = self.user
        order.status_id = OrderStatus.retrieve_id('new')
        order.date_start = timezone.now()
        if CartItemRepository().get_user_cart(self.user.pk).exists():
            order.save()
        return order
