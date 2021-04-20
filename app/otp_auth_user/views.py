from os import stat
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import SigninUserSerializer, UserSerializer
from .models import Token, User, generate_verification_code
from .authentications import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupUserView(CreateAPIView):
    """ Signup/create a new user in system """
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """ sends a verification code after user created """
        user = serializer.save()
        print(user.verification_code)


class RequestVCodeView(APIView):
    """ Generates an verification code, saves it in users model
        and sends it through sms """

    def post(self, request):
        """ Check if user is exists then send a verification code """
        phone = request.data["phone"]
        user = get_object_or_404(get_user_model(), phone=phone)
        user.verification_code = generate_verification_code()
        print(user.verification_code)
        user.save()

        return Response({"msg": "verification code is sent."})


class SigninUserView(CreateAPIView):
    serializer_class = SigninUserSerializer

    def create(self, request):
        phone = request.data["phone"]
        vcode = request.data["verification_code"]
        user = get_object_or_404(get_user_model(),
                                 phone=phone,
                                 verification_code=vcode)

        token = get_tokens_for_user(user)

        Token.objects.create(user=user, **token)

        user.verification_code = ""
        user.save()
        data = {
            "token": token
        }
        return Response(data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """ Retrieve authenticated user profile"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
