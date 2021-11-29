from django.db import models

from apps.api.api_order.models import Order
from apps.api.api_product.models import Product


class ShoppingCart(models.Model):
    class Meta:
        db_table = 'shopping_cart'
    unique_together = (('product', 'order'),)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()