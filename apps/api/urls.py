from django.urls import path, include
from .api_user import urls as api_user_urlpatterns


urlpatterns = [
    path('api_user/', include(api_user_urlpatterns)),
]