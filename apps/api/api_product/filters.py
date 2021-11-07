import django_filters

from apps.api.api_product.models import Product, ProductType, Vendor


class ProductFilter(django_filters.FilterSet):
    product_type = django_filters.ModelChoiceFilter(queryset=ProductType.objects.all())
    product_price = django_filters.RangeFilter()
    product_vendor = django_filters.ModelMultipleChoiceFilter(
        queryset=Vendor.objects.all()
    )

    class Meta:
        model = Product
        fields = ['product_price', 'product_type', 'product_vendor']