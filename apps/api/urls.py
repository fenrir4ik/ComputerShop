from django.urls import path, include

from .api_loader import ApiLoader
from .api_user import urls as api_user_urlpatterns
from .api_product import urls as api_product_urlpatterns
from .views import ApiRepository

urlpatterns = [
    path('api_user/', include(api_user_urlpatterns)),
    path('api_product/', include(api_product_urlpatterns)),
    path('', ApiRepository.as_view(), name='API Repository')
]

ApiLoader.load_api(urlpatterns, clear_db=True)