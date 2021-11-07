import django_filters

from apps.api.api_product.models import Product, ProductType


class ProductFilter(django_filters.FilterSet):
    product_type = django_filters.ModelChoiceFilter(queryset=ProductType.objects.all())
    product_price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['product_price', 'product_type']