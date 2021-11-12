from rest_framework import serializers

from .models import Product, ProductType, ProductCharacteristics


class ProductCharacteristicsDisplaySerializer(serializers.ModelSerializer):
    char_name = serializers.StringRelatedField(source='char', read_only=True)

    class Meta:
        model = ProductCharacteristics
        fields = ['char_value', 'char_name']


class ProductCharacteristicsSerializer(serializers.Serializer):
    char_value = serializers.CharField(required=True)
    char_name = serializers.CharField(required=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['product_characteristics']


class ProductSerializerDisplay(serializers.ModelSerializer):
    product_type = serializers.StringRelatedField()
    product_vendor = serializers.StringRelatedField()
    product_characteristics = ProductCharacteristicsDisplaySerializer(source='productcharacteristics_set', many=True)

    class Meta:
        model = Product
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class DictionaryWrapper(object):
    def __init__(self, dictionary):
        self.dict = dictionary
