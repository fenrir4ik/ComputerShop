from django.db.models import OuterRef, Subquery, Q, QuerySet

from apps.store.models import Product, ProductPrice, ProductImage, CartItem


class ProductDao:
    @staticmethod
    def get_products_list(include_price: bool = True, include_image: bool = True) -> QuerySet:
        products = Product.objects.select_related('vendor', 'category')
        if include_price:
            products = ProductDao.annotate_queryset_with_price(products)
        if include_image:
            products = ProductDao.annotate_queryset_with_image(products)
        return products

    @staticmethod
    def annotate_queryset_with_price(queryset, ref: str = 'pk', actual: bool = True) -> QuerySet:
        price = ProductPrice.objects.filter(product=OuterRef(ref)).order_by('-date_actual')
        if not actual:
            price = price.filter(date_actual__lte=OuterRef('order__date_start'))
        queryset = queryset.annotate(price=Subquery(price.values('price')[:1]))
        return queryset

    @staticmethod
    def annotate_queryset_with_image(queryset, ref: str = 'pk') -> QuerySet:
        product_image = ProductImage.objects.filter(Q(product=OuterRef(ref)) & Q(is_main=True))
        queryset = queryset.annotate(image=Subquery(product_image.values('image')[:1]))
        return queryset

    @staticmethod
    def delete_product(product_id: int) -> bool:
        try:
            cart_lookup = CartItem.objects.filter(product_id=OuterRef('pk')).values('product_id')
            return Product.objects.filter(pk=product_id) \
                .exclude(pk__in=Subquery(cart_lookup)) \
                .get(pk=product_id) \
                .delete()
        except Product.DoesNotExist:
            return False
