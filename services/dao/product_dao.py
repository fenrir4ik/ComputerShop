from django.db.models import OuterRef, Subquery, Q, QuerySet

from apps.store.models import Product, ProductPrice, ProductImage


class ProductDAO:
    @staticmethod
    def get_products_list(include_price: bool = True, include_image: bool = True) -> QuerySet:
        products = Product.objects.select_related('vendor', 'category')
        if include_price:
            actual_price = ProductPrice.objects.filter(product=OuterRef('pk')).order_by('-date_actual')
            products = products.annotate(price=Subquery(actual_price.values('price')[:1]))
        if include_image:
            product_image = ProductImage.objects.filter(Q(product=OuterRef('pk')) & Q(is_main=True))
            products = products.annotate(image=Subquery(product_image.values('image')[:1]))
        return products

    @staticmethod
    def delete_product(product: Product):
        # check if product exists in carts
        product.delete()
