from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model




def sample_user(phone="+989123456789", full_name="testname"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


class UserModelTests(TestCase):
    def test_create_user_successful(self):
        """ Test create a user successfuly """
        phone = "+989123456789"
        full_name = "testname"
        user = sample_user(phone, full_name)

        self.assertTrue(bool(user.base32_key))
        self.assertEqual(user.phone, phone)

    def test_create_user_invalid_phone_number(self):
        """ Test creating a user with an invalid phone number """

        with self.assertRaises(ValueError):
            user = sample_user(phone=None)

        with self.assertRaises(ValidationError):
            user1 = sample_user(phone="invalidPhoneNumber")
            user2 = sample_user(phone="0123456780")
            user3 = sample_user(phone="1235")

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
