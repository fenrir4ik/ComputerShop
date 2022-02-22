import django_filters

from apps.store.filters import ProductFilter
from apps.store.models import Product


class AdminProductFilter(ProductFilter):
    date_created = django_filters.DateRangeFilter()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'category', 'vendor']
    # date_created - date_range
    # css remove from left panel

    def __init__(self, data=None, queryset=None, **kwargs):
        super().__init__(data, queryset, **kwargs)

