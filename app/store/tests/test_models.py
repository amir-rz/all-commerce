from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .. import models
from core import models as core_models


def sample_user(phone="+989123456789", full_name="testname"):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name)


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)
        self.website_category = core_models.WebsiteCategory.objects.create(
            name="Clothing")

    def test_store_str_repr(self):
        """ Test store string representation"""

        city = models.City.objects.create(name="london")

        store = models.Store.objects.create(
            name="Nike",
            owner=self.user,
            description="delivers innovative products, experiences and services to inspire athletes.",
            address="NikeTown London. 236 Oxford St. London, W1C 1DE",
            lat=24.2343,
            long=-15.123,
            city=city
        )

        self.assertEqual(str(store), store.name)

    def test_city_str_repr(self):
        """ Test store string representation """
        city = models.City.objects.create(name="london")

        self.assertEqual(str(city), city.name)

    def test_category_str_repr(self):
        """ Test category string representation """
        category = models.Category.objects.create(
            name="Shoes", website_category=self.website_category)
        self.assertEqual(str(category), category.name)

    def test_brand_str_repr(self):
        """ Test brand string representation """
        category = models.Category.objects.create(
            name="Shoes", website_category=self.website_category)
        brand = models.Brand.objects.create(
            name_fa="نایک",
            name_en="nike",
            category=category
        )
        self.assertEqual(str(brand), f"{brand.name_fa} - {brand.name_en}")

    def test_product_str_repr(self):
        """ Test product string representation """
        category = models.Category.objects.create(
            name="Shoes", website_category=self.website_category)
        brand = models.Brand.objects.create(
            name_fa="نایک",
            name_en="nike",
            category=category
        )
        product = models.Product.objects.create(
            name="Adapt BB",
            brand=brand,
            purchased_price=500000,
            sale_price=600000,
            discount=9,
            stock=500,
            weight_in_grams=300,
            in_bulk=False,
            colors="000,fff",
            category=category,
        )

        self.assertEqual(str(product), product.name)

    def test_sub_category_str_repr(self):
        """
        Test create sub category and string representation.
        if "website_category" is not provided, then parent "website_category"
        """
        category = models.Category.objects.create(
            name="Shoes", website_category=self.website_category)
        sub_category = models.Category.objects.create(
            name="Sandal", parent_category=category,
            website_category=self.website_category
        )
        self.assertEqual(str(sub_category), sub_category.name)
