from rest_framework import permissions


class UpdateInformation(permissions.BasePermission):
    """Allow only staff to make changes"""

    def has_permission(self, request, view):
        """Check user trying to edit is staff"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
