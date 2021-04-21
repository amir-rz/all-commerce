from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AnonymousUser

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber

from rest_framework_simplejwt.tokens import RefreshToken

from random import randint


def generate_verification_code():
    """ Generates a 5 digit integer, verification code """
    return randint(10000, 99999)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserManager(BaseUserManager):

    def create_user(self, phone, full_name, password=None, **extra_fields):

        validate_international_phonenumber(phone)

        if not phone:
            raise ValueError("a phone number must be provided.")

        user = self.model(
            phone=phone,
            full_name=full_name,
            verification_code=generate_verification_code(),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):

        user = self.create_user(phone=phone,
                                full_name=phone,
                                password=password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    phone = PhoneNumberField(unique=True)
    full_name = models.CharField(max_length=255)
    verification_code = models.CharField(default="",
                                         max_length=5)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.full_name
