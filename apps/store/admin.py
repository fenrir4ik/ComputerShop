from django.contrib import admin

from apps.store.models import Vendor, Category, PaymentType, OrderStatus

admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(PaymentType)
admin.site.register(OrderStatus)
