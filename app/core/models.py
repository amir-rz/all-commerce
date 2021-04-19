from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber

from random import randint


def generate_verification_code():
    """ Generates a 5 digit integer, verification code """
    return randint(10000, 99999)


class UserManager(BaseUserManager):

    def create_user(self, phone, full_name, password=None, **extra_fields):

        validate_international_phonenumber(phone)

        if not phone:
            raise ValueError("a phone number must be provided.")

        user = self.model(
            phone=phone,
            full_name=full_name,

            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        validate_international_phonenumber(phone)

        user = self.create_user(phone,
                                password,
                                **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    phone = PhoneNumberField(unique=True)
    full_name = models.CharField(max_length=255)
    verification_code = models.IntegerField(default=generate_verification_code(),
                                            validators=[MinValueValidator(5),
                                                        MaxValueValidator(5)])
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() 

    USERNAME_FIELD = "phone"

    def save(self, *args, **kwargs):

        if type(self.verification_code) == "str":
            raise ValidationError("Verification code cannot be string")

        if len(str(self.verification_code)) > 5 or len(str(self.verification_code)) < 5:
            raise ValidationError("Verification code must be 5 digit number")

        super().save(*args, **kwargs)
