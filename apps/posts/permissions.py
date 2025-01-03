from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow any read request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write operations require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user can view the post
        if request.method in permissions.SAFE_METHODS:
            return obj.status == 'published' or (request.user and request.user.is_authenticated and obj.author == request.user)

        # Write permissions are only allowed to the author of the post
        return obj.author == request.user
