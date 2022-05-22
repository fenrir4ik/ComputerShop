from typing import Union

from django.apps import apps
from django.db import transaction
from django.db.models import F, OuterRef, Subquery, QuerySet

from db.order_repository import OrderRepository
from db.product_repository import ProductRepository


class CartItemRepository:
    def __init__(self):
        self.CartItem = apps.get_model('store', 'CartItem')
        self.Product = apps.get_model('store', 'Product')

    def get_product_amount_in_cart_by_user_id(self, user_id: int, product_id) -> int:
        """Returns product amount in cart of user with given user id"""
        cart_id = OrderRepository().get_user_cart_id(user_id)
        return self.get_product_amount_in_cart(cart_id, product_id)

    def get_product_amount_in_cart(self, cart_id: int, product_id: int) -> int:
        """Returns product amount in cart of user with given cart id"""
        try:
            cart_item = self.CartItem.objects.get(order_id=cart_id, product_id=product_id)
            return cart_item.amount
        except self.CartItem.DoesNotExist:
            return 0

    def add_product_to_cart(self, cart_id: int, product_id: int, amount: int):
        """Adds given amount of product to user cart with given cart_id"""
        with transaction.atomic():
            self.CartItem.objects.create(order_id=cart_id, product_id=product_id, amount=amount)
            self.Product.objects.filter(pk=product_id).update(amount=F('amount') - amount)

    def change_product_in_cart(self, cart_id: int, product_id: int, amount_difference: int):
        """
        Changes amount of product in user cart using amount_difference
        Positive difference means that user have chosen more product amount that it was before
        Negative difference means that user have chosen less product amount that it was before
        """
        with transaction.atomic():
            self.CartItem.objects.filter(order_id=cart_id, product_id=product_id) \
                .update(amount=F('amount') + amount_difference)
            self.Product.objects.filter(pk=product_id).update(amount=F('amount') - amount_difference)

    def delete_products_in_cart(self, cart_id: int, products_id: Union[int, QuerySet]):
        """
        Deletes given products from user cart Accepts products_id as integer or QuerySet,
        performs casting either types into list() and processes it atomically
        """
        if isinstance(products_id, int):
            products_id = [products_id]
        else:
            products_id = list(products_id)
        with transaction.atomic():
            cart_item = self.CartItem.objects.filter(order_id=cart_id, product_id__in=products_id).select_for_update()
            self.Product.objects.filter(pk__in=products_id) \
                .update(amount=F('amount') + Subquery(cart_item.filter(product_id=OuterRef('pk')).values('amount')))
            cart_item.delete()

    def get_user_cart(self, user_id: int) -> QuerySet:
        """Returns user cart including products, their images and prices"""
        product_repository = ProductRepository()
        cart_id = OrderRepository().get_user_cart_id(user_id)
        user_cart = self.CartItem.objects.filter(order_id=cart_id).select_related('product')
        user_cart = product_repository.annotate_queryset_with_image(user_cart, ref='product_id')
        user_cart = product_repository.annotate_queryset_with_price(user_cart, ref='product_id')
        return user_cart

    def get_cart_products_id(self, cart_id: int) -> QuerySet:
        return self.CartItem.objects.filter(order_id=cart_id).values_list('product_id', flat=True)
