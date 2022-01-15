from django.urls import path

from apps.user.views import login_, logout_, index

urlpatterns = [
    path('', index),
    path('login/', login_),
    path('logout/', logout_)
]
