from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

from .models import Token


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        access_token = request.META.get("HTTP_AUTHORIZATION")

        if not access_token:
            raise exceptions.NotAuthenticated("Unauthenticated")

        access_token = access_token.split(" ")[1]

        try:
            token = Token.objects.get(access=access_token)

        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        user = token.user
        token = token.access
        return (user, token)

    # def authenticate_header(self, request):
    #     print(request)
    #     return super().authenticate_header(request)