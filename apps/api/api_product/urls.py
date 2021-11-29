from django.urls import path

from .views import ProductViewSet, ProductCharacteristicsAPI, ProductTypeAPI


product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

app_name = 'Product API'

urlpatterns = [
    path('product/', product_list, name='Product List'),
    path('product/<int:pk>/', product_detail, name='Product Details'),
    path('product_characteristics/<int:pk>/', ProductCharacteristicsAPI.as_view(), name='Product Characteristics'),
    path('product_types/', ProductTypeAPI.as_view(), name='Product Types')
]