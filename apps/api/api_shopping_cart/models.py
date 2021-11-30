from django.db import models

from apps.api.api_order.models import Order
from apps.api.api_product.models import Product


class ShoppingCart(models.Model):
    class Meta:
        db_table = 'shopping_cart'
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte='1'), name='amount_positive'),
        ]
    unique_together = (('product', 'order'),)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=False, null=False, )