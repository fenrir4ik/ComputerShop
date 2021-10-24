from apps.api_user.views import UserViewSet
from rest_framework import routers


class ApiUserRouter(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        root_view = super(ApiUserRouter, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__name__ = "api_user"
        root_view.cls.__doc__ = "API for user registration and authentication"
        return root_view


router = ApiUserRouter()
router.register(r'users', UserViewSet)
