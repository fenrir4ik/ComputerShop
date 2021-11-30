from django.urls import path

from apps.api.api_shopping_cart.views import ShoppingCartAPI, DeleteProductAPI, ClearCartAPI, OrderCartAPI

app_name = 'Shopping Cart API'

urlpatterns = [
    path('cart/', ShoppingCartAPI.as_view(), name='Cart'),
    path('clear_cart/', ClearCartAPI.as_view(), name='Clear Cart'),
    path('cart/<int:pk>/', DeleteProductAPI.as_view(), name='Remove Product From Cart'),
    path('order_cart/<int:pk>/', OrderCartAPI.as_view(), name='Get Order Cart')
]
