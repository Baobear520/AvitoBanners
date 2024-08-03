from rest_framework.permissions import BasePermission

class IsSelfOrAdmin(BasePermission):
    """
    Custom permission to only allow users to access their own profile
    or allow admins to access any profile.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin or accessing their own profile
        return request.user.is_staff or obj.user == request.user


   