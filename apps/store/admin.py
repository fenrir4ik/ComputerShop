from django.contrib import admin

from apps.store.models import Vendor, Category

admin.site.register(Vendor)
admin.site.register(Category)