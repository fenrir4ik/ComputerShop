from django.urls import path

from apps.client.views import index

urlpatterns = [
    path('test/', index),
]
