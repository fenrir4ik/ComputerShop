from django.urls import path

from .views import RegisterAPI, LoginAPI, ChangePasswordAPI, LogoutAPI


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change_password/', ChangePasswordAPI.as_view(), name='change-password'),
]