from django.urls import path

from apps.admin_panel.views import ProductAddView, ProductsListAdminView

urlpatterns = [
    path('products/new/', ProductAddView.as_view(), name='add product'),
    path('products/', ProductsListAdminView.as_view(), name='admin products'),
    # path('products/<int:pk>/delete'),
    # path('products/<int:pk>/'),
    # path('orders/'),
    # path('orders/<int:pk>/'),
]