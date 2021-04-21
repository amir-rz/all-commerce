from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """ Only allows users that verified (is_verified=True) """

    def has_permission(self, request, view):
        return request.user.is_verified
