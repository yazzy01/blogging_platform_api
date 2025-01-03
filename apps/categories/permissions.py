from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit categories.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff
