from django import forms


class AddProductToCartForm(forms.Form):
    def __init__(self, amount_in_cart, max_amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        amount_in_cart = None if amount_in_cart < 1 else amount_in_cart
        self.fields['amount'] = forms.IntegerField(label="Кол-во",
                                                   min_value=1,
                                                   max_value=max_amount,
                                                   initial=amount_in_cart)
