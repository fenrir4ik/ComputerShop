from django.urls import path

from .views import RegisterAPI, LoginAPI, ChangePasswordAPI, LogoutAPI

app_name = 'User API'

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='Login'),
    path('logout/', LogoutAPI.as_view(), name='Logout'),
    path('register/', RegisterAPI.as_view(), name='Registration'),
    path('change_password/', ChangePasswordAPI.as_view(), name='Change Password')
]
