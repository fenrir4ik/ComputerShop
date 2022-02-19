from django.contrib import admin

from apps.store.models import Vendor, Category, PaymentType

admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(PaymentType)
