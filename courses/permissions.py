from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom Permission To check if object owner is the request user or not along with admin check
    """

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return True if obj.teacher.user == request.user or request.user.is_superuser else False
