from django.urls import path

from apps.user.views import UserRegister, UserLogin, UserLogout

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('register/', UserRegister.as_view(), name='registration')
]
