from rest_framework import permissions

class IsDoctorAndOwner(permissions.BasePermission):
    """
    Allow access only to doctors for their own patients.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user 