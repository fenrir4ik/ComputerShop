from django.db.models import OuterRef, Subquery, Q, QuerySet

from apps.store.models import Product, ProductPrice, ProductImage


class ProductDAO:
    @staticmethod
    def get_products_list(include_price: bool = True, include_image: bool = True) -> QuerySet:
        products = Product.objects.select_related('vendor', 'category')
        if include_price:
            products = ProductDAO.annotate_queryset_with_price(products)
        if include_image:
            products = ProductDAO.annotate_queryset_with_image(products)
        return products

    @staticmethod
    def annotate_queryset_with_price(queryset, ref='pk') -> QuerySet:
        actual_price = ProductPrice.objects.filter(product=OuterRef(ref)).order_by('-date_actual')
        queryset = queryset.annotate(price=Subquery(actual_price.values('price')[:1]))
        return queryset

    @staticmethod
    def annotate_queryset_with_image(queryset, ref='pk') -> QuerySet:
        product_image = ProductImage.objects.filter(Q(product=OuterRef(ref)) & Q(is_main=True))
        queryset = queryset.annotate(image=Subquery(product_image.values('image')[:1]))
        return queryset

    @staticmethod
    def delete_product(product: Product):
        # check if product exists in carts
        # replace product with product_id in future
        product.delete()
