from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


    # product_type
    # product_vendor
    # product_characteristics
    # product_name
    # product_price
    # product_amount
    # product_description
    # product_image