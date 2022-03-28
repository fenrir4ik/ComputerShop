from typing import Union

from django.db import transaction
from django.db.models import F, OuterRef, Subquery, QuerySet

from apps.store.models import CartItem, Product
from db.order_dao import OrderDAO
from db.product_dao import ProductDAO


class CartItemDAO:
    """DAO is used to interact with CartItem model instances"""

    @staticmethod
    def get_product_amount_in_cart_by_user_id(user_id: int, product_id) -> int:
        """Returns product amount in cart of user with given user id"""
        cart_id = OrderDAO.get_user_cart_id(user_id)
        return CartItemDAO.get_product_amount_in_cart(cart_id, product_id)

    @staticmethod
    def get_product_amount_in_cart(cart_id: int, product_id: int) -> int:
        """Returns product amount in cart of user with given cart id"""
        try:
            cart_item = CartItem.objects.get(order_id=cart_id, product_id=product_id)
            return cart_item.amount
        except CartItem.DoesNotExist:
            return 0

    @staticmethod
    def add_product_to_cart(cart_id: int, product_id: int, amount: int):
        """Adds given amount of product to user cart with given cart_id"""
        with transaction.atomic():
            CartItem.objects.create(order_id=cart_id, product_id=product_id, amount=amount)
            Product.objects.filter(pk=product_id).update(amount=F('amount') - amount)

    @staticmethod
    def change_product_in_cart(cart_id: int, product_id: int, amount_difference: int):
        """
        Changes amount of product in user cart using amount_difference
        Positive difference means that user have chosen more product amount that it was before
        Negative difference means that user have chosen less product amount that it was before
        """
        with transaction.atomic():
            CartItem.objects.filter(order_id=cart_id, product_id=product_id).update(
                amount=F('amount') + amount_difference)
            Product.objects.filter(pk=product_id).update(amount=F('amount') - amount_difference)

    @staticmethod
    def delete_products_in_cart(cart_id: int, products_id: Union[int, QuerySet]):
        """
        Deletes given products from user cart Accepts products_id as integer or QuerySet,
        performs casting either types into list() and processes it atomically
        """
        if isinstance(products_id, int):
            products_id = [products_id]
        else:
            products_id = list(products_id)
        with transaction.atomic():
            cart_item = CartItem.objects.filter(order_id=cart_id, product_id__in=products_id).select_for_update()
            Product.objects.filter(pk__in=products_id) \
                .update(amount=F('amount') + Subquery(cart_item.filter(product_id=OuterRef('pk')).values('amount')))
            cart_item.delete()

    @staticmethod
    def get_user_cart(user_id: int) -> QuerySet:
        """Returns user cart including products, their images and prices"""
        cart_id = OrderDAO.get_user_cart_id(user_id)
        user_cart = CartItem.objects.filter(order_id=cart_id).select_related('product')
        user_cart = ProductDAO.annotate_queryset_with_image(user_cart, ref='product_id')
        user_cart = ProductDAO.annotate_queryset_with_price(user_cart, ref='product_id')
        return user_cart
