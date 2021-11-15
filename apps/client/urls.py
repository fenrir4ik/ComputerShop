from django.urls import path


from apps.client.views import login, logout, index

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('', index),
]
