from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.api.views import APIBaseView
from .filters import OrderFilter
from .models import Order, OrderStatus, PaymentType
from .permissions import ClientPermission
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, PaymentTypeSerializer, \
    OrderStatusSerializer
from ..api_shopping_cart.models import ShoppingCart


class OrderViewSet(viewsets.ModelViewSet, APIBaseView):
    queryset = Order.objects.exclude(order_status=None).order_by('id').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ['=id', '=to_telno', '=to_email', '=to_surname', '=to_name']
    ordering_fields = ['order_date', 'order_status']
    ordering = ['order_date']
    http_method_names = ['get', 'post', 'put', 'patch']
    permission_classes = [IsAuthenticated & ClientPermission]

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            permission_classes = [IsAdminUser]
        elif self.action in ('post',):
            permission_classes = [IsAuthenticated & ClientPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('create',):
            return CreateOrderSerializer
        elif self.action in ('update', 'partial_update'):
            return UpdateOrderSerializer
        else:
            return OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        if not order.order_status:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_staff and request.user.id != order.user_id:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        orders = self.filter_queryset(self.get_queryset())
        if not request.user.is_staff:
            orders = orders.filter(user=request.user)
        paginated_orders = self.paginate_queryset(orders)
        serializer = self.get_serializer(paginated_orders, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                order = Order.objects.filter(user=request.user, order_status=None).select_for_update().get()
                if order:
                    if not ShoppingCart.objects.filter(order=order).exists():
                        return Response({'detail': 'Shopping cart is empty'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        order.order_status = OrderStatus.objects.get(status_name='Новый')
                        order.payment_type = PaymentType.objects.get(pk=serializer.data.get('payment_type'))
                        order.order_date = timezone.now().date()
                        order.to_name = serializer.data.get('to_name')
                        order.to_surname = serializer.data.get('to_surname')
                        order.to_email = serializer.data.get('to_email')
                        order.to_telno = serializer.data.get('to_telno')
                        order.address = serializer.data.get('address')
                        order.save()
                        return Response(data={'order_id': order.id})
                else:
                    raise Exception()
        except:
            return Response({'detail': 'User has no shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def document(cls, **kwargs) -> dict:
        if not kwargs.get("details", False):
            cls.doc = {
                'get': {'in': {}, 'out': {}},
                'post': {'in': {}, 'out': {}}
            }
        else:
            cls.doc = {
                'get': {'in': {}, 'out': {}},
                'put': {'in': {}, 'out': {}},
                'patch': {'in': {}, 'out': {}},
                'delete': {'in': {}, 'out': {}}
            }
        return super(OrderViewSet, cls).document()


class PaymentTypeAPI(generics.ListAPIView, APIBaseView):
    serializer_class = PaymentTypeSerializer
    permission_classes = (AllowAny,)
    queryset = PaymentType.objects.all()
    pagination_class = None
    http_method_names = ['get']

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'get': {'in': {}, 'out': {'list': {'id': 'integer', 'type': 'string'}} }
        }
        return super(PaymentTypeAPI, cls).document()


class OrderStatusAPI(generics.ListAPIView, APIBaseView):
    serializer_class = OrderStatusSerializer
    permission_classes = (AllowAny,)
    queryset = OrderStatus.objects.all()
    pagination_class = None
    http_method_names = ['get']

    @classmethod
    def document(cls) -> dict:
        cls.doc = {
            'get': {'in': {}, 'out': {'list': {'id': 'integer', 'status_name': 'string'}} }
        }
        return super(OrderStatusAPI, cls).document()