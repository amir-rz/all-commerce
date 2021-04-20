from django.core.exceptions import ValidationError
from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework.test import APIClient
from rest_framework import status

from ..models import Token


def sample_user(phone="+989123456789", full_name="testname"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


REQUEST_VCODE_URL = reverse("user:request-vcode")
SIGNIN_URL = reverse("user:signin")
SIGNUP_URL = reverse("user:signup")


class PublicUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_signup_user(self):
        """ Test sign up a user """
        payload = {
            "phone": "+989123456780",
            "full_name": "test_name"
        }
        res = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_signup_user_invalid_phone_number(self):
        """ Test signing up a user with an invalid number """
        payload = {
            "phone": "09123456780",
            "full_name": "testName"
        }

        res = self.client.post(SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_vcode_for_user(self):
        """ Test request a verification code in order to signin the user"""
        user = sample_user()
        payload = {
            "phone": user.phone
        }
        res = self.client.post(REQUEST_VCODE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_signin_a_user(self):
        """ Test signin a user with recived verification code through sms """
        user = sample_user()
        payload = {
            "phone": user.phone,
            "verification_code": user.verification_code
        }

        res = self.client.post(SIGNIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_signin_user_invalid_vcode(self):
        """ Test sign in a user with invalid verifciation code """
        user = sample_user()

        payload = {
            "phone": user.phone,
            "verification_code": int(user.verification_code) + 1
        }

        res = self.client.post(SIGNIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn("token", res.data)

    def test_vcode_is_null_after_signin(self):
        """ Test that verification code is null after user 
        signed in successfuly """
        user = sample_user()

        payload = {
            "phone": user.phone,
            "verification_code": user.verification_code
        }
        res = self.client.post(SIGNIN_URL, payload)
        user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user.verification_code, "")

    def test_token_is_saved_in_system(self):
        """ Test token is saved in db after user signed in """
        user = sample_user()

        payload = {
            "phone": user.phone,
            "verification_code": user.verification_code
        }

        res = self.client.post(SIGNIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user=user)

        self.assertNotEqual(len(token.access), 0)


class PrivateUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    