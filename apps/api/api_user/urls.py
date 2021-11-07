from django.urls import path

from .views import RegisterAPI, LoginAPI, ChangePasswordAPI, LogoutAPI
from ..views import SingleApiList

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='Login'),
    path('logout/', LogoutAPI.as_view(), name='Logout'),
    path('register/', RegisterAPI.as_view(), name='Registration'),
    path('change_password/', ChangePasswordAPI.as_view(), name='Password Changing'),
]

urlpatterns.append(path('', SingleApiList.as_view(urlpatterns=urlpatterns.copy()), name='User API'))
