from django.contrib.auth.models import User
from rest_framework import permissions


class ClientPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        not_admin = User.objects.filter(id=user.id, is_staff=False).exists()
        return not_admin
