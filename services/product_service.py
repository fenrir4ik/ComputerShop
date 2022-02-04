from django.db.models import OuterRef, Subquery, Q

from apps.store.models import Product, ProductPrice, ProductImage


class ProductManager():
    @property
    def get_products_list(self):
        actual_price = ProductPrice.objects.filter(product=OuterRef('pk')).order_by('-date_actual')
        product_image = ProductImage.objects.filter(Q(product=OuterRef('pk')) & Q(is_main=True))
        products = Product.objects.select_related('vendor', 'category') \
            .annotate(price=Subquery(actual_price.values('price')[:1])) \
            .annotate(image=Subquery(product_image.values('image')[:1]))
        return products

