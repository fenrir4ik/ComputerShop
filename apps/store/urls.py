from django.urls import path

from apps.store.views import IndexView, ProductAddView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add-product/', ProductAddView.as_view(), name='add product')
]
