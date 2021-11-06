from django.urls import path

from .views import RegisterAPI, LoginAPI, ChangePasswordAPI, LogoutAPI
from ..views import SingleApiList

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change_password/', ChangePasswordAPI.as_view(), name='change_password'),
]

urlpatterns.append(path('', SingleApiList.as_view(urlpatterns=urlpatterns.copy()), name='single_api_list'))
