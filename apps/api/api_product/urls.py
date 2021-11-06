from django.urls import path
from .views import ProductViewSet
from ..views import SingleApiList


#TODO   +product/
#       +product/?page=2
#       -product/?page=2&type=5!!!!
#       +product/2 GET
#       +product/2 POST
#       +product/2 DELETE
#       +product/2 UPDATE
#       -characteristics GET/POST/DELETE/UPDATE
#       +GET CHARACTERISTICS PER TYPE

product_list = ProductViewSet.as_view({
    'get': 'list'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
    'post': 'create'
})

urlpatterns = [
    path('product/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_details')
]

urlpatterns.append(path('', SingleApiList.as_view(urlpatterns=urlpatterns.copy()), name='single_api_list'))
