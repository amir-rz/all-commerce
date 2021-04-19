from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import User


def sample_user(phone="+989123456789", full_name="testname", password="userpass"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name,
                                                password=password)


class ModelTests(TestCase):

    def test_create_user_successful(self):
        """ Test create a user successfuly """
        phone = "+989123456789"
        full_name = "testname"
        password = "testpass"
        user = sample_user(phone, full_name, password)

        self.assertTrue(bool(user.password))
        self.assertEqual(user.phone, phone)
        self.assertTrue(user.check_password(password))

    def test_create_user_invalid_phone_number(self):
        """ Test creating a user with an invalid phone number """

        with self.assertRaises(ValueError):
            user = sample_user(phone=None)

        with self.assertRaises(ValidationError):
            user1 = sample_user(phone="invalidPhoneNumber")
            user2 = sample_user(phone="0123456780")
            user3 = sample_user(phone="1235")

    def test_user_recieve_a_valid_verification_code(self):
        """ Test that user gets a valid verification code after user created. """
        user = sample_user()

        self.assertEqual(len(str(user.verification_code)), 5)
        self.assertTrue(bool(user.verification_code))

    def test_user_verification_code_cannot_accept_str(self):
        """ Test user verification_code field cannot be string """
        user = sample_user()
        with self.assertRaises(ValidationError):
            user.verification_code = "string"
            user.save()

    def test_user_invalid_number_verification_code(self):
        """ Test invalid verification code """

        with self.assertRaises(ValidationError):
            user = sample_user()
            user.verification_code = 123
            user.save()

    def test_create_superuser_successful(self):
        """ Test create a superuser successfuly """
        phone = "+989123456780"
        password = "admin"
        user = get_user_model().objects.create_superuser(
            phone=phone,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
