import django_filters

from apps.store.filters import ProductFilter, BaseOrderFilter
from apps.store.models import Product, Order


class AdminProductFilter(ProductFilter):
    id = django_filters.NumberFilter(label="Идентификатор товара")
    date_created = django_filters.DateRangeFilter()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'category', 'vendor']

    def __init__(self, data=None, queryset=None, **kwargs):
        super().__init__(data, queryset, **kwargs)


class AdminOrderFilter(BaseOrderFilter):
    id = django_filters.CharFilter(label="Поиск по номеру заказа", method="search_by_id")
    phone_number = django_filters.CharFilter(label="Поиск по номеру телефона", method="search_by_phone_number")
    email = django_filters.CharFilter(label="Поиск по электронному адресу", method="search_by_email")

    class Meta:
        model = Order
        fields = ['id', 'phone_number', 'email', 'date_end', 'status']

    def search_by_id(self, queryset, name, value):
        try:
            return queryset.filter(id=value)
        except ValueError:
            return queryset

    def search_by_phone_number(self, queryset, name, value):
        return queryset.filter(phone_number__iexact=value)

    def search_by_email(self, queryset, name, value):
        return queryset.filter(email__iexact=value)