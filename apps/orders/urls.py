from django.urls import path

from .views import orders_list, order_details

urlpatterns = [
    path('orders/', orders_list, name='orders'),
    path('orders/<int:pk>/', order_details, name='order details')
]
