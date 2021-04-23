from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from .. import models


def sample_user(phone="+989123456789", full_name="testname"):
    """ Create and return a user instance """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


def sample_city(name="london"):
    """ Create and return a city instance """
    return models.City.objects.create(name=name)


def sample_store(user, city, name="Nike", is_verified=False):
    """ Create and return an store instance"""
    return models.Store.objects.create(
        name=name,
        owner=user,
        description="delivers innovative products, experiences and services to inspire athletes.",
        address="NikeTown London. 236 Oxford St. London, W1C 1DE",
        lat=22.2343,
        long=-13.123,
        city=city,
        is_verified=is_verified
    )


STORE_URL = reverse("store:store-list")


def detail_url(pk, endpoint_name: str = "store", **kwargs):
    """
    returns a detail url + pk for given endpoint,
    e.g. /stores/pro-nike
    """
    return reverse(f"store:{endpoint_name}-detail", args=[pk], kwargs=kwargs)


class StorePublicApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.city = sample_city()

    def test_list_all_stores(self):
        """ Test list all available stores """
        store1 = sample_store(sample_user(), self.city)
        store2 = sample_store(sample_user(
            phone="+989123456788"), self.city)

        res = self.client.get(STORE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class StorePrivateApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.city = sample_city()
        self.client.force_authenticate(user=self.user)

    def test_user_list_stores(self):
        """ Test list all stores that authenticated user owns """
        sample_store(self.user, self.city)
        res = self.client.get(STORE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(res.data), 0)

    def test_user_update_own_store(self):
        """ Test that user can only update their own store profile """
        user2 = sample_user("+989123456500")
        store = sample_store(user2, city=self.city)

        payload = {"is_open": True}

        res = self.client.patch(detail_url(store.id), payload)
        store.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(store.is_open, False)

    def test_any_update_unverifies_the_store(self):
        """ 
        Test that any update to store makes is_verified to False
        so it needs to get verified again
        """
        store = sample_store(self.user, self.city, is_verified=True)
        payload = {"description": "new description"}

        self.assertTrue(store.is_verified)

        res = self.client.patch(detail_url(store.id), payload)
        store.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(store.is_verified)
