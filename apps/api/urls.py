from django.urls import path, include


from .api_user import urls as api_user_urlpatterns
from .api_product import urls as api_product_urlpatterns
from .api_order import urls as api_order_urlpatterns
from .api_shopping_cart import urls as api_shopping_cart_urlpatterns

urlpatterns = [
    path('api_user/', include(api_user_urlpatterns)),
    path('api_product/', include(api_product_urlpatterns)),
    path('api_order/', include(api_order_urlpatterns)),
    path('api_shopping_cart/', include(api_shopping_cart_urlpatterns))
]
