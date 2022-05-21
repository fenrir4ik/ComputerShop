from django.apps import apps
from django.db.models import OuterRef, Subquery, Q, QuerySet, F, Min, Max


class ProductRepository:
    def __init__(self):
        self.Product = apps.get_model('store', 'Product')
        self.CartItem = apps.get_model('store', 'CartItem')
        self.ProductPrice = apps.get_model('store', 'ProductPrice')
        self.ProductImage = apps.get_model('store', 'ProductImage')
        self.Characteristic = apps.get_model('store', 'Characteristic')

    def get_products_list(self, include_price: bool = True, include_image: bool = True) -> QuerySet:
        """Returns product list with optional annotation with price and image"""
        products = self.Product.objects.select_related('vendor', 'category')
        if include_price:
            products = self.annotate_queryset_with_price(products)
        if include_image:
            products = self.annotate_queryset_with_image(products)
        return products

    def annotate_queryset_with_price(self, queryset: QuerySet, ref: str = 'pk', actual: bool = True) -> QuerySet:
        """Annotates given queryset of products with price, using ref as OuterRef"""
        price = self.ProductPrice.objects.filter(product=OuterRef(ref)).order_by('-date_actual')
        if not actual:
            price = price.filter(date_actual__lte=OuterRef('order__date_start'))
        queryset = queryset.annotate(price=Subquery(price.values('price')[:1]))
        return queryset

    def annotate_queryset_with_image(self, queryset: QuerySet, ref: str = 'pk') -> QuerySet:
        """Annotates given queryset of products with image, using ref as OuterRef"""
        product_image = self.ProductImage.objects.filter(Q(product=OuterRef(ref)) & Q(is_main=True))
        queryset = queryset.annotate(image=Subquery(product_image.values('image')[:1]))
        return queryset

    def delete_product(self, product_id: int) -> bool:
        """
        Deletes product from system and returns True if deletion is done
        If product exists in user cart, False is returned
        """
        try:
            cart_lookup = self.CartItem.objects.filter(product_id=OuterRef('pk')).values('product_id')
            product = self.Product.objects.filter(pk=product_id) \
                .exclude(pk__in=Subquery(cart_lookup)) \
                .get(pk=product_id)
            deleted = product.delete()
            if deleted:
                self.Characteristic.objects.filter(products=None).delete()
            return deleted
        except self.Product.DoesNotExist:
            return False

    def update_product_rating(self, product_id: int, rating: float):
        self.Product.objects.filter(pk=product_id).update(rating=F('rating') + rating)

    def get_min_max_product_rating(self) -> tuple:
        minmax_rating = self.Product.objects.aggregate(Min('rating'), Max('rating'))
        return minmax_rating.get('rating__min'), minmax_rating.get('rating__max')
