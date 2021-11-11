from django.urls import path, include
from .api_user import urls as api_user_urlpatterns
from .api_product import urls as api_product_urlpatterns


urlpatterns = [
    path('api_user/', include(api_user_urlpatterns), name='User API'),
    path('api_product/', include(api_product_urlpatterns), name='Product API'),
]
