from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.user.models import User


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    exclude = ('username',)
    list_display = ('id', 'email', 'phone_number', 'date_joined')
    search_fields = ('email', 'phone_number')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    ordering = ()
