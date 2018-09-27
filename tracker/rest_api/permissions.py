from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    The request is admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
        )


class IsSuperAdmin(permissions.BasePermission):
    """
    The request by super admin only
    """

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_superuser
        )
