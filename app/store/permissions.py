from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "Only owner can update store"

    def has_object_permission(self, request, view, obj):
        """ Only owner can update the store """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsStoreOwnerToUpdate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Check if the current user is the owner of store """

        if request.method == "PATCH" or request.method == "PUT":
            print(obj.store.owner == request.user)
            return obj.store.owner == request.user

        return True
