import django_filters
from django import forms

from apps.store.models import Product, Category, Vendor
from db.vendor_dao import VendorDAO


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple(),
                                                        queryset=Category.objects.all())
    name = django_filters.CharFilter(
        lookup_expr='contains',
        widget=forms.TextInput(attrs={'id': 'searchline', 'placeholder': 'Поиск товара...'})
    )
    price = django_filters.RangeFilter(label='Цена')
    vendor = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple())
    sort = django_filters.OrderingFilter(
        choices=(
            ('price', 'от дешевых к дорогим'),
            ('-price', 'от дорогих к дешевым'),
            ('name', 'по алфавиту'),
            ('date_created', 'новинки')
        )
    )

    class Meta:
        model = Product
        fields = ['category', 'vendor']

    def __init__(self, data=None, queryset=None, **kwargs):
        super().__init__(data, queryset, **kwargs)
        category_list = data.getlist('category')
        if category_list:
            self.filters['vendor'].queryset = VendorDAO.get_vendors_for_product_category(category_list)
        else:
            self.filters['vendor'].queryset = Vendor.objects.none()
