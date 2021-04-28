from core.helpers import VerifyInstancePhoneNumber, get_tokens_for_user
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (RequestVCodeSerializer, SigninUserSerializer,
                          UserSerializer, VerificationCodeSerializer)


class CreateAndSigninUser(ListCreateAPIView):
    """ This is just for development ,
        creates a user + a token
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(phone=request.data["phone"])
            serializer = self.get_serializer(user)
            token = get_tokens_for_user(user)
            data = {
                "user": serializer.data,
                "token": token
            }
            return Response(data)
        except get_user_model().DoesNotExist:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                user = get_object_or_404(
                    get_user_model(), pk=serializer.data["id"])
                token = get_tokens_for_user(user)
                data = {
                    "user": serializer.data,
                    "token": token
                }
                return Response(data)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupUserView(CreateAPIView):
    """ Signup/create a new user in system """
    serializer_class = UserSerializer


class RequestVCodeView(CreateAPIView):
    """ Generates an verification code, saves it in users model
        and sends it through sms """
    serializer_class = RequestVCodeSerializer

    def create(self, request):
        """ Check if user is exists then send a verification code """
        phone = request.data["phone"]
        if not phone:
            raise ValueError("A phone number must be provided")
        user = get_object_or_404(get_user_model(), phone=phone)

        verify_phone = VerifyInstancePhoneNumber(get_user_model(), user)
        verify_phone.request_verification()

        return Response({"msg": "verification code is sent."})


class ObtainToken(CreateAPIView):
    """ Obtain a new jwt token for user """
    serializer_class = SigninUserSerializer

    def create(self, request):
        phone = request.data["phone"]
        vcode = request.data["verification_code"]

        user = get_object_or_404(get_user_model(), phone=phone)
        verify_phone = VerifyInstancePhoneNumber(get_user_model(), user)

        if verify_phone.submit_verification(verification_code=vcode):
            token = get_tokens_for_user(user)

            data = {
                "token": token
            }
            return Response(data)

        return Response({"msg": "Verification is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """ Retrieve authenticated user profile"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if "phone" in data:
            if data["phone"] != user.phone:
                verify_phone = VerifyInstancePhoneNumber(
                    get_user_model(), user)
                verify_phone.request_verification()
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
    serializer_class = VerificationCodeSerializer
    # 63498

    def create(self, request):
        """ 
        Verifies the phone number that user provided
        by send a verification code through sms
        """
        user = request.user
        vcode = request.data["verification_code"]

        if not vcode:
            return Response({"msg": "Verification code is not provided."}, status=status.HTTP_400_BAD_REQUEST)

        verify_phone = VerifyInstancePhoneNumber(get_user_model(), user)

        if verify_phone.submit_verification(verification_code=vcode):
            return Response({"Phone number is verified."})

        return Response({"msg": "Verification code is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
