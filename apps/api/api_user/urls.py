from django.urls import path

from .views import RegisterAPI, LoginAPI, ChangePasswordAPI, LogoutAPI


urlpatterns = [
    path(LoginAPI.set_call_path('login/'), LoginAPI.as_view(), name='login'),
    path(LogoutAPI.set_call_path('logout/'), LogoutAPI.as_view(), name='logout'),
    path(RegisterAPI.set_call_path('register/'), RegisterAPI.as_view(), name='register'),
    path(ChangePasswordAPI.set_call_path('change_password/'), ChangePasswordAPI.as_view(), name='change-password'),
]

# print(RegisterAPI.get_api_details())
# print(LoginAPI.get_api_details())
# print(ChangePasswordAPI.get_api_details())
# print(LogoutAPI.get_api_details())