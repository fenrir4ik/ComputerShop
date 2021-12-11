from django.urls import path

from .views import delete, edit, add

urlpatterns = [
    path('add/', add, name='add product'),
    path('edit/<int:pk>/', edit, name='edit product'),
    path('delete/<int:pk>/', delete, name='delete product'),
]
