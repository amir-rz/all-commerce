import os
import tempfile
from unittest.mock import patch

from core import models as core_models
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from rest_framework.test import APIClient

from .. import models


def sample_user(phone="+989123456789", full_name="testname", phone_is_verified=False):
    """ Create a sample user """
    return get_user_model().objects.create_user(phone=phone,
                                                full_name=full_name,
                                                phone_is_verified=phone_is_verified)


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


def sample_website_category(name="Clothing"):
    """ Creates and returns a website category instance """
    return core_models.WebsiteCategory.objects.create(
        name=name
    )


def sample_category(website_category, name="Shoes", owner=None, is_verified=False):
    """ Creates and returns a category instance """

    return models.Category.objects.create(
        name=name,
        website_category=website_category,
        owner=owner,
        is_verified=is_verified
    )


def sample_sub_category(parent_category, website_category, name="Sandal", owner=None, is_verified=False):
    """ Creates and returns a sub category instance """

    return models.Category.objects.create(
        name=name,
        website_category=website_category,
        parent_category=parent_category,
        owner=owner,
        is_verified=is_verified
    )


def sample_brand(category=None, name_fa="نایک", name_en="", is_verified=False, owner=None):
    """ Creates and returns a brand instance """
    return models.Brand.objects.create(
        name_fa=name_fa,
        name_en=name_en,
        is_verified=is_verified,
        owner=owner
    )


def sample_product(brand,
                   category,
                   store,
                   name="Nike Adapt BB",
                   purchased_price=500000,
                   sale_price=600000,
                   discount=9,
                   stock=50,
                   is_verified=False
                   ):
    """ Creates and returns a product instance """
    return models.Product.objects.create(
        name=name,
        purchased_price=purchased_price,
        sale_price=sale_price,
        discount=discount,
        stock=stock,
        brand=brand,
        category=category,
        store=store,
        is_verified=is_verified

    )


def sample_supermarket_product(brand,
                               category,
                               store,
                               name="Nike Adapt BB",
                               purchased_price=500000,
                               sale_price=600000,
                               discount=9,
                               stock=50,
                               weight_in_grams=0,
                               in_bulk=False,
                               is_verified=False):
    """ Creates and returns a product instance """
    return models.SupermarketProduct.objects.create(
        name=name,
        purchased_price=purchased_price,
        sale_price=sale_price,
        discount=discount,
        stock=stock,
        weight_in_grams=weight_in_grams,
        in_bulk=in_bulk,
        brand=brand,
        category=category,
        store=store,
        is_verified=is_verified
    )


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(user=self.user)
        self.city = sample_city()
        self.store = sample_store(self.user, self.city)
        self.website_category = sample_website_category()
        self.category = sample_category(self.website_category)
        self.sub_category = sample_sub_category(
            self.category, self.website_category)
        self.brand = sample_brand(self.category)
        self.product = sample_product(self.brand, self.category, self.store)
        self.supermarket_product = sample_supermarket_product(
            self.brand, self.category, self.store)

    def test_store_str_repr(self):
        """ Test store string representation"""

        self.assertEqual(str(self.store), self.store.name)

    def test_city_str_repr(self):
        """ Test store string representation """

        self.assertEqual(str(self.city), self.city.name)

    def test_category_str_repr(self):
        """ Test category string representation """

        self.assertEqual(str(self.category), self.category.name)

    def test_sub_category_str_repr(self):
        """
        Test create sub category and string representation.
        if "website_category" is not provided, then parent "website_category"
        """

        self.assertEqual(str(self.sub_category), self.sub_category.name)

    def test_brand_str_repr(self):
        """ Test brand string representation """

        self.assertEqual(str(self.brand), self.brand.name_fa)

    def test_product_str_repr(self):
        """ Test product string representation """

        self.assertEqual(str(self.product), self.product.name)

    def test_supermarket_product_str_repr(self):
        """ Test supermarket product string representation """

        self.assertEqual(str(self.supermarket_product),
                         self.supermarket_product.name)

    @patch("uuid.uuid4")
    def test_product_file_name_uuid(self, mock_uuid):
        """ Test that image is saved in the correct location """
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, "myimage.jpg")

        exp_path = f"uploads/product/{uuid}.jpg"
        self.assertEqual(file_path, exp_path)
