from django import forms


class AddProductToCartForm(forms.Form):
    def __init__(self, max_amount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(label="Кол-во", min_value=1, max_value=max_amount)
