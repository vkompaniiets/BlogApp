from django.core.exceptions import PermissionDenied


class AdminPermissionMixin(object):
    def has_permissions(self):
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
        return super(AdminPermissionMixin, self).dispatch(request, *args, **kwargs)
