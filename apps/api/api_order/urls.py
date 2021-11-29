from django.urls import path
from .views import OrderViewSet, ShoppingCartGetAPI

#   +api_order/orders
#   +api_order/orders    filter by time, status, search by id
#   +api_order/orders    POST (create order) | Not admin, cart exists, get or create by user id
#   +api_order/orders/{id} GET
#   +api_order/orders/{id} PATCH (change status etc)
#   +api_order/orders/{id} PUT (change order)
#   +api_order/orders/shopping_cart/ POST (create cart)

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
    path('order/shopping_cart/', ShoppingCartGetAPI.as_view(), name='Get Shopping Cart')
]
