from django import forms

from apps.store.forms import CheckoutForm


class StatusForm(forms.Form):
    order_status = forms.ChoiceField(choices=[])

class OrderDetailsForm(CheckoutForm, StatusForm):
    order_date = forms.CharField(disabled=True, required=False)

