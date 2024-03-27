from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """
    Custom permission to only allow doctors to access the data.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a doctor
        return request.user.is_authenticated and request.user.is_doctor