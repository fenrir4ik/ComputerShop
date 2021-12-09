from rest_framework import serializers

from .models import ShoppingCart
from ..api_product.models import Product


class ProductDisplayInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_price', 'product_image']
        depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = ProductDisplayInCartSerializer()

    class Meta:
        model = ShoppingCart
        fields = ['amount', 'product']


class ProductAddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ['amount', 'product']