from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """ Only allows users that verified (phone_is_verified=True) """

    def has_permission(self, request, view):
        return request.user.phone_is_verified
