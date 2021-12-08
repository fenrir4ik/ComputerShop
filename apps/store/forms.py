from django import forms


class SearchForm(forms.Form):
    search_request = forms.CharField(required=False)
