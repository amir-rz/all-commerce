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


def sample_store(name="Nike",user=sample_user()):
    """ Create and return an store instance"""
    return models.Store.objects.create(
        name="Nike",
        owner=user,
        description="delivers innovative products, experiences and services to inspire athletes.",
        phone="+151234567890",
        address="NikeTown London. 236 Oxford St. London, W1C 1DE",
        lat=2234.2343,
        lon=-123.123,
        city=sample_city()
    )


STORE_URL = reverse("store:store-list")


def detail_url(endpoint_name: str, slug):
    """
    returns a detail url + pk for given endpoint,
    e.g. /stores/pro-nike
    """
    return reverse(f"{endpoint_name}-detail", args=[slug])


class StorePrivateApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_user_list_stores(self):
        """ Test list all stores that authenticated user owns """
        sample_store(user=self.user)
        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(res.data), 0)
