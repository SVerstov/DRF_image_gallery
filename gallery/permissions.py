from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ unsafe method only for owner """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminUserOrCantDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'POST'):
            return True
        return bool(request.user and request.user.is_staff)
