from django.conf.urls import url
from django.urls import path, include

from .api_loader import ApiLoader
from .api_user import urls as api_user_urlpatterns
from .api_product import urls as api_product_urlpatterns
from .api_order import urls as api_order_urlpatterns
from .api_shopping_cart import urls as api_shopping_cart_urlpatterns
from .views import ApiRepository
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Computer Shop API",
      default_version='v1',
      description="Computer Shop API endpoints",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api_user/', include(api_user_urlpatterns)),
    path('api_product/', include(api_product_urlpatterns)),
    path('api_order/', include(api_order_urlpatterns)),
    path('shopping_cart/', include(api_shopping_cart_urlpatterns)),
    path('', ApiRepository.as_view(), name='API Repository'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

ApiLoader.load_api(urlpatterns)
