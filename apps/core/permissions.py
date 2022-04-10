import abc

from django.http import HttpResponseForbidden
#PermissionRequiredMixin

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
        return self.request.user.is_authenticated and not self.request.user.is_staff


class ManagerPermissionMixin(BasePermission):
    # raise_exception = False
    def has_permission(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
