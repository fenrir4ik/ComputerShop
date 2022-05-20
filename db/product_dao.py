from django.db.models import OuterRef, Subquery, Q, QuerySet, F, Min, Max

import apps.store.models as models


class ProductDAO:
    """DAO is used to interact with Product model instances"""

    @staticmethod
    def get_products_list(include_price: bool = True, include_image: bool = True) -> QuerySet:
        """Returns product list with optional annotation with price and image"""
        products = models.Product.objects.select_related('vendor', 'category')
        if include_price:
            products = ProductDAO.annotate_queryset_with_price(products)
        if include_image:
            products = ProductDAO.annotate_queryset_with_image(products)
        return products

    @staticmethod
    def annotate_queryset_with_price(queryset: QuerySet, ref: str = 'pk', actual: bool = True) -> QuerySet:
        """Annotates given queryset of products with price, using ref as OuterRef"""
        price = models.ProductPrice.objects.filter(product=OuterRef(ref)).order_by('-date_actual')
        if not actual:
            price = price.filter(date_actual__lte=OuterRef('order__date_start'))
        queryset = queryset.annotate(price=Subquery(price.values('price')[:1]))
        return queryset

    @staticmethod
    def annotate_queryset_with_image(queryset: QuerySet, ref: str = 'pk') -> QuerySet:
        """Annotates given queryset of products with image, using ref as OuterRef"""
        product_image = models.ProductImage.objects.filter(Q(product=OuterRef(ref)) & Q(is_main=True))
        queryset = queryset.annotate(image=Subquery(product_image.values('image')[:1]))
        return queryset

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """
        Deletes product from system and returns True if deletion is done
        If product exists in user cart, False is returned
        """
        try:
            cart_lookup = models.CartItem.objects.filter(product_id=OuterRef('pk')).values('product_id')
            product = models.Product.objects.filter(pk=product_id) \
                .exclude(pk__in=Subquery(cart_lookup)) \
                .get(pk=product_id)
            deleted = product.delete()
            if deleted:
                models.Characteristic.objects.filter(products=None).delete()
            return deleted
        except models.Product.DoesNotExist:
            return False

    @staticmethod
    def update_product_rating(product_id: int, rating: float):
        models.Product.objects.filter(pk=product_id).update(rating=F('rating') + rating)

    @staticmethod
    def get_min_max_product_rating() -> tuple:
        minmax_rating = models.Product.objects.aggregate(Min('rating'), Max('rating'))
        return minmax_rating.get('rating__min'), minmax_rating.get('rating__max')
