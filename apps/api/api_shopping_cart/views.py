from django.db import connection
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ShoppingCart
from .permissions import ClientPermission
from .serializers import ShoppingCartSerializer
from ..api_order.models import Order


class ShoppingCartAPI(generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    http_method_names = ['get', 'put', 'post']
    permission_classes = [IsAuthenticated & ClientPermission]

    def get_serializer_class(self):
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = self.get_queryset().filter(order__user=user, order__order_status=None).all()
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data.get('amount')
        product_id = serializer.data.get('product')
        if amount > 0:
            try:
                with connection.cursor() as cursor:
                    Order.objects.get_or_create(user=request.user, order_status=None)
                    cursor.execute(f"call add_product_to_cart({product_id}, {user_id}, {amount})")
            except:
                return Response({'detail': 'Internal error. Wrong amount or product_id'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Wrong product amount'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'amount': amount, 'product_id': product_id}, status=status.HTTP_201_CREATED)


class ClearCartAPI(generics.DestroyAPIView):
    http_method_names = ['delete']
    permission_classes = [IsAuthenticated & ClientPermission]

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"call clear_cart({user_id})")
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Internal error'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteProductAPI(generics.DestroyAPIView):
    http_method_names = ['delete']
    permission_classes = [IsAuthenticated & ClientPermission]

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        product_id = kwargs.get('pk')
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"call del_product_from_cart({product_id}, {user_id})")
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Internal error'}, status=status.HTTP_400_BAD_REQUEST)


class OrderCartAPI(generics.RetrieveAPIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        order_id = kwargs.get('pk')

        # check if order belongs to user and if it is created
        if (not Order.objects.filter(id=order_id).exclude(order_status=None).exists()) or \
                (not user.is_staff and not Order.objects.filter(id=order_id, user=user).exists()):
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        cart = self.get_queryset().filter(order_id=order_id).all()
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)
