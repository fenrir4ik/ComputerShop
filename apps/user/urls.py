from django.urls import path

from apps.user.views import login_, logout_, UserRegister


urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', logout_, name='logout'),
    path('register/', UserRegister.as_view(), name='registration')
]
