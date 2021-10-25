from django.urls import path
from knox import views as knox_views

from .views import RegisterAPI, LoginAPI, ChangePasswordView

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
]