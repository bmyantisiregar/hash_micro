from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


class RolePermissionMixin():
    role_permissions = {
        'manager': ['add_product', 'change_product', 'delete_product', 'view_product'],
        'user': ['add_product', 'change_product', 'view_product'],
        'public': ['view_product'],
    }

    required_permission = None

    def dispatch(self, request, *args, **kwargs):
        # Get all groups the user belongs to
        user_groups = request.user.groups.values_list('name', flat=True)

        # Check if user belongs to any defined role group
        for group in user_groups:
            perms = self.role_permissions.get(group, [])
            if self.required_permission in perms:
                return super().dispatch(request, *args, **kwargs)

        # If not allowed
        raise PermissionDenied("You don't have permission to perform this action.")
