from django.db import models
from django.contrib.auth.models import User

class OrderStatus(models.Model):
    class Meta:
        db_table = 'order_status'

    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_name


class Order(models.Model):
    class Meta:
        db_table = 'order'

    user = models.ForeignKey(User, models.RESTRICT)
    order_status = models.ForeignKey(OrderStatus, models.RESTRICT, null=True)
    order_date = models.DateField(blank=True, null=True, db_index=True)
    to_name = models.CharField(max_length=30, db_index=True)
    to_telno = models.CharField(max_length=30, db_index=True)
    to_surname = models.CharField(max_length=30, db_index=True)
    to_email = models.EmailField(db_index=True)
    address = models.CharField(max_length=255, blank=True, null=True)


