from django.urls import path

from apps.store.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('mycart/<int:pk>/delete/', ProductDeleteFromCartView.as_view(), name='delete-cart-item'),
    path('mycart/', UserCartView.as_view(), name='user-cart'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', UserOrdersListView.as_view(), name='user-orders'),
]
