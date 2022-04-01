from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated or
                request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'moderator':
            return True
        return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return False
