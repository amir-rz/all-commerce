from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "Only owner can update store"

    def has_object_permission(self, request, view, obj):
        """ Only owner can update the store """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
