import abc

from django.http import HttpResponseForbidden

from apps.core.models import UserRole


class BasePermission(abc.ABC):
    @abc.abstractmethod
    def has_permission(self):
        pass

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CustomerPermission(BasePermission):
    def has_permission(self):
        if self.request.user.is_authenticated:
            return not self.request.user.role
        else:
            return False


class ManagerPermissionMixin(BasePermission):
    raise_exception = False

    def has_permission(self):
        if self.request.user.is_authenticated:
            return self.request.user.has_role(UserRole.MANAGER)
        else:
            return False


class WarehousePermissionMixin(ManagerPermissionMixin):
    def has_permission(self):
        is_authenticated_manager = super().has_permission()
        if self.request.user.is_authenticated:
            return is_authenticated_manager or self.request.user.has_role(UserRole.WAREHOUSE_WORKER)
        else:
            return False
