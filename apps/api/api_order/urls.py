from django.urls import path
from .views import OrderViewSet, PaymentTypeAPI, OrderStatusAPI

order_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

order_detail = OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

app_name = 'Order API'

urlpatterns = [
    path('order/', order_list, name='Order List'),
    path('order/<int:pk>/', order_detail, name='Order Details'),
    path('payment_types/', PaymentTypeAPI.as_view(), name='Payment Types'),
    path('orders_status/', OrderStatusAPI.as_view(), name='Orders Status')
]
