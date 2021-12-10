from django.conf.urls import url
from django.urls import path

from .views import index, product_details, product_remove, shopping_cart, checkout, clear_cart


urlpatterns = [
    url(r'^$', index, name='index'),
    path('product_details/<int:pk>/', product_details, name='product details'),
    path('product_details/delete/<int:pk>/', product_remove, name='remove from cart'),
    path('shopping_cart/', shopping_cart, name='shopping cart'),
    path('checkout/', checkout, name='checkout'),
    path('clear_shopping_cart/', clear_cart, name='clear shopping cart')
]
