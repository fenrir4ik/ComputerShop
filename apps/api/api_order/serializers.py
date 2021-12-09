from rest_framework import serializers

from .models import Order, PaymentType, OrderStatus


class OrderSerializer(serializers.ModelSerializer):
    order_status = serializers.StringRelatedField(read_only=True)
    payment_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['order_date', 'user', 'order_status']


class UpdateOrderSerializer(CreateOrderSerializer):
    class Meta:
        model = Order
        exclude = ['order_date', 'user']
        extra_kwargs = {'order_status': {'required': True, 'allow_null': False}}


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'