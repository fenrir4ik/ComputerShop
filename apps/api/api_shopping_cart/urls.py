from django.urls import path


from apps.api.api_shopping_cart.views import TestApi

#       ~product_add/{id} POST {id_product, amount}
#       ~product_delete/{id} POST {id_order, id_product}
#       ~product_change/{id} PATCH
#       product_get/{id}  GET
#       product_in_carts  GET !!! НУЖЕН АТОМИК
#       ~clear/{id}
#       cart_is_empty/{id} проверка есть ли товары в корзине

app_name = 'Shopping Cart API'

urlpatterns = [
    path('test/', TestApi.as_view(), name='Test'),
]
