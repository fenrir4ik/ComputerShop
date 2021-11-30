from django.urls import path

from apps.api.api_shopping_cart.views import ShoppingCartAPI, DeleteProductAPI, ClearCartAPI


#       product_in_carts  GET !!! НУЖЕН АТОМИК

#       cart_is_empty/{id} проверка есть ли товары в корзине В order перенести


app_name = 'Shopping Cart API'

urlpatterns = [
    path('cart/', ShoppingCartAPI.as_view(), name='Cart'),
    path('cart/clear_cart/', ClearCartAPI.as_view(), name='Clear Cart'),
    path('cart/<int:pk>/', DeleteProductAPI.as_view(), name='Remove Product From Cart')
]
