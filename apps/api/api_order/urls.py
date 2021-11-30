from django.urls import path
from .views import OrderViewSet

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
    path('order/<int:pk>/', order_detail, name='Order Details')
]
