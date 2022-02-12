from django.urls import path

from apps.store.views import IndexView, ProductDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product detail'),
    # get cart (user)
    # clear cart (user)
    # add to cart (user)
    # delete from cart (user)
    # change in cart (user)
    # create cart (user)
    # create order (user)
    # list order (user)
    # order details (user)
    # list order (admin)
    # change order (admin)
]
