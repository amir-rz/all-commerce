from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from ..models import Store, City


def sample_user(phone="+989123456789", full_name="testname"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)

    def test_store_str(self):
        """ Test create a new store successfully """

        city = City.objects.create(name="london")
   
        store = Store.objects.create(
            name="Nike",
            owner=self.user,
            description="delivers innovative products, experiences and services to inspire athletes.",
            phone="+151234567890",
            address="NikeTown London. 236 Oxford St. London, W1C 1DE",
            lat=2234.2343,
            lon=-123.123,
            city=city
        )

        self.assertEqual(str(store), store.name)

    def test_create_city_successful(self):
        """ Test create city successfully """
        city = City.objects.create()

        self.assertEqual(str(city), city.name)
