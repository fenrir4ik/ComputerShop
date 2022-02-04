from django.urls import path

from apps.store.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
