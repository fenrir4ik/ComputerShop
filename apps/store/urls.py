from django.conf.urls import url
from django.urls import path

from .views import index, details


urlpatterns = [
    url(r'^$', index, name='index'),
    path('product_details/<int:pk>/', details, name='product details'),
]
