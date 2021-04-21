from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from ..models import generate_totp_for_user

import pyotp


REQUEST_VCODE_URL = reverse("user:request-vcode")
SIGNUP_URL = reverse("user:signup")
TOKEN_URL = reverse("user:obtain-token")
TOKEN_REFRESH_URL = reverse("user:token-refresh")
PROFILE_URL = reverse("user:profile")
VERIFY_PHONE_NUMBER = reverse("user:verify-phone-number")


def sample_user(phone="+989123456789", full_name="testname"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


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

    def test_request_vcode_for_non_existing_user(self):
        """ Test request vcode for non existing user """
        payload = {
            "phone": "+98123456780"
        }
        res = self.client.post(REQUEST_VCODE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_signin_a_user(self):
        """ Test signin a user with recived verification code through sms """
        user = sample_user()
        vcode = generate_totp_for_user(user).now()

        payload = {
            "phone": user.phone,
            "verification_code": vcode
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_signin_user_invalid_vcode(self):
        """ Test sign in a user with invalid verifciation code """
        user = sample_user()
        vcode = generate_totp_for_user(user).now()

        payload = {
            "phone": user.phone,
            "verification_code": int(vcode) + 1
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)


class PrivateUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve_own_profile(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("phone", res.data)

    def test_user_update_own_profile(self):
        """ Test user is able to update/put hes own profile """
        current_name = self.user.full_name
        new_name = "newname"
        payload = {
            "phone": self.user.phone,
            "full_name": new_name
        }

        res = self.client.put(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(current_name, res.data["full_name"])

    def test_user_update_same_phone_number(self):
        """ 
        Test if user updated phone number 
        but with the same value, the nothing happens/is_verified=True
        """
        self.user.is_verified = True
        payload = {"phone": self.user.phone}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_user_update_and_verify_new_phone_number(self):
        """ Test user needs to verify the new phone number 
            if the phone number is different than current one
         """
        payload = {"phone": "+989123456781"}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("phone", res.data)
        self.assertEqual(res.data["phone"], payload["phone"])
        self.assertFalse(self.user.is_verified)
        
        vcode = generate_totp_for_user(self.user).now()
        payload = {
            "verification_code": vcode
        }

        res = self.client.post(VERIFY_PHONE_NUMBER, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_verified)

    def test_refresh_token(self):
        """ Test recieve a new access and refresh for current refresh token  """
        vcode = generate_totp_for_user(self.user).now()
     
        payload = {
            "phone": self.user.phone,
            "verification_code": vcode
        }
        res = self.client.post(TOKEN_URL, payload)
        payload = {
            "refresh": res.data["token"]["refresh"]
        }
        res = self.client.post(TOKEN_REFRESH_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)


