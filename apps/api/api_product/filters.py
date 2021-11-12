import django_filters

from apps.api.api_product.models import Product, ProductType, Vendor


class ProductFilter(django_filters.FilterSet):
    product_type = django_filters.ModelChoiceFilter(queryset=ProductType.objects.all())
    product_price = django_filters.RangeFilter()
    product_vendor = django_filters.ModelMultipleChoiceFilter()

    class Meta:
        model = Product
        fields = ['product_price', 'product_type', 'product_vendor']

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        product_type = kwargs['data'].get('product_type')
        if product_type:
            self.filters['product_vendor'].queryset = Vendor.objects.filter(products__product_type_id=product_type).distinct()
        else:
            self.filters['product_vendor'].queryset = Vendor.objects.none()
