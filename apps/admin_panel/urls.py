from django.urls import path

from apps.admin_panel.views import ProductAddView, ProductsListAdminView, ProductDeleteView, ProductUpdateView

urlpatterns = [
    path('products/', ProductsListAdminView.as_view(), name='admin products'),
    path('products/new/', ProductAddView.as_view(), name='add product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete product'),
    path('products/<int:pk>/', ProductUpdateView.as_view(), name='update product'),
    # list order (admin)
    # change order (admin)
]
