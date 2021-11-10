from django.urls import path

from .views import ProductViewSet, ProductCharacteristicsAPI, ProductTypeAPI
from ..views import SingleApiList

#TODO   ++product/
#       ++product/?page=2
#       ++product/?page=2&type=5&asc desc&!!!!
#       ++product/2 GET
#       ++product/ POST
#       ++product/2 DELETE
#       ++product/2 UPDATE
#       ++characteristics POST/DELETE/UPDATE TO PRODUCT
#       ++get all types

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


urlpatterns = [
    path('product/', product_list, name='Products List'),
    path('product/<int:pk>/', product_detail, name='Product Details'),
    path('product_characteristics/<int:pk>/', ProductCharacteristicsAPI.as_view(), name='Product Characteristics'),
    path('product_types/', ProductTypeAPI.as_view(), name='Product Type List')
]

urlpatterns.append(path('', SingleApiList.as_view(urlpatterns=urlpatterns.copy()), name='Product API'))
