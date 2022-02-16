from django.urls import path

from apps.admin_panel.views import *

urlpatterns = [
    path('products/', ProductsListAdminView.as_view(), name='admin-products'),
    path('products/new/', ProductAddView.as_view(), name='product-add'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    # list order (admin)
    # change order (admin)
]
