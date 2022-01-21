from django.urls import path

from apps.user.views import UserRegisterView, UserLoginView, UserLogoutView, ProfileChangeView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('profile/', ProfileChangeView.as_view(), name='profile')
]
