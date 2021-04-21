from os import stat
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import SigninUserSerializer, UserSerializer, RequestVCodeSerializer, VerifyNewPhoneNumberSerializer
from .models import User, get_tokens_for_user

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainSerializer

import pyotp
import time


class SignupUserView(CreateAPIView):
    """ Signup/create a new user in system """
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """ sends a verification code after user created """
        user = serializer.save()


class RequestVCodeView(CreateAPIView):
    """ Generates an verification code, saves it in users model
        and sends it through sms """
    serializer_class = RequestVCodeSerializer

    def create(self, request):
        """ Check if user is exists then send a verification code """
        phone = request.data["phone"]
        user = get_object_or_404(get_user_model(), phone=phone)

        otp_vcode = pyotp.TOTP(user.key, 5, interval=600)
        print(f"{user.phone}: {otp_vcode.now()}")
        user.save()

        return Response({"msg": "verification code is sent."})


class ObtainToken(CreateAPIView):
    """ Obtain a new jwt token for user """
    serializer_class = SigninUserSerializer

    def create(self, request):
        phone = request.data["phone"]
        vcode = request.data["verification_code"]

        user = get_object_or_404(User, phone=phone)

        totp = pyotp.TOTP(user.key, 5, interval=30,)

        if totp.verify(vcode):
            token = get_tokens_for_user(user)

            user.verification_code = ""
            user.is_verified = True
            user.save()
            data = {
                "token": token
            }
            return Response(data)

        return Response({"msg": "Verification is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """ Retrieve authenticated user profile"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if "phone" in data:
            if data["phone"] != user.phone:
                user.is_verified = False
                user.save()
                print(user.verification_code)
            else:
                pass
        return super().partial_update(request, *args, **kwargs)


class VerifyNewPhoneNumberView(CreateAPIView):
    """ 
    Users must verify new phone number when they change their current phone
    number
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyNewPhoneNumberSerializer
    # 63498

    def create(self, request):
        """ 
        Verifies the phone number that user provided
        by send a verification code through sms
        """
        user = request.user
        data = request.data
        if not data["verification_code"]:
            return Response({"msg": "Verification code is not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code == data["verification_code"]:
            user.verification_code = ""
            user.is_verified = True
            user.save()
            return Response({"Phone number is verified."})

        return Response({"msg": "Verification code is wrong."}, status=status.HTTP_400_BAD_REQUEST)
