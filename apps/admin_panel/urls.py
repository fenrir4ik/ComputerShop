from django.urls import path

from apps.admin_panel.views import *

urlpatterns = [
    path('products/', ProductsListAdminView.as_view(), name='admin-products'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('orders/', OrdersListView.as_view(), name='admin-orders'),
    path('orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
]
