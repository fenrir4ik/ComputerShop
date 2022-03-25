import django_filters
from django import forms
from django.db.models import Q
from django_filters.widgets import RangeWidget

from apps.store.models import Product, Category, Vendor, Order
from db.vendor_dao import VendorDAO


class FromToRangeWidget(django_filters.widgets.RangeWidget):
    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super().__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple(),
                                                        queryset=Category.objects.all())
    keyword = django_filters.CharFilter(
        label='Ключевые слова',
        method='search_by_keyword',
        widget=forms.TextInput(attrs={'id': 'searchline', 'placeholder': 'Поиск товара...'}),

    )
    price = django_filters.RangeFilter(
        label='Цена',
        widget=FromToRangeWidget(from_attrs={'placeholder': 'минимальная', 'type': 'number'},
                                 to_attrs={'placeholder': 'максимальная', 'type': 'number'})
    )
    vendor = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple())
    sort = django_filters.OrderingFilter(
        label="Отсортировать",
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

    def search_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class BaseOrderFilter(django_filters.FilterSet):
    date_end = django_filters.DateRangeFilter(label="Дата завершения")

    class Meta:
        model = Order
        fields = ['date_end']


class OrderFilter(BaseOrderFilter):
    keyword = django_filters.CharFilter(label="Поиск по всем заказам", method="search_by_keyword")

    def search_by_keyword(self, queryset, name, value):
        queryset_filtered_by_id = self.filter_queryset_by_id(queryset, value)
        queryset_filtered_by_products_names = self.filter_queryset_by_products_name(queryset, value)
        return queryset_filtered_by_id.union(queryset_filtered_by_products_names)

    def filter_queryset_by_id(self, queryset, value):
        try:
            return queryset.filter(id=value)
        except ValueError:
            return queryset.none()

    def filter_queryset_by_products_name(self, queryset, value):
        return queryset.filter(products__name__icontains=value)
