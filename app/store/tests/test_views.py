from .. import views
import os
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .. import models
from . import test_models as smpl

STORES_LIST_URL = reverse("store:store-list")
CATEGORIES_LIST_URL = reverse("store:category-list")
BRAND_LIST_URL = reverse("store:brand-list")
SUPERMARKET_PRODUCT_LIST_URL = reverse("store:supermarket-product-list")
PRODUCT_IMAGE_UPLOAD_URL = reverse("store:upload-product-image-list")
WISH_LIST_URL = reverse("store:wish-list-item-list")


def detail_url(pk, endpoint_name: str = "store", **kwargs):
    """
    returns a detail url + pk for given endpoint,
    e.g. /stores/pro-nike
    """
    return reverse(f"store:{endpoint_name}-detail", args=[pk], kwargs=kwargs)


class StorePublicApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.city = smpl.sample_city()
        self.store_category = smpl.sample_store_category()

    # Store
    def test_list_only_verified_stores(self):
        """
        Test to ensure that only verified stores will be listed,
        for unauthenticated users or those that doesnt own the store
        """

        smpl.sample_store(smpl.sample_user(), self.store_category, self.city)
        smpl.sample_store(smpl.sample_user(
            phone="+989123456788"), self.store_category, self.city, is_verified=True)

        res = self.client.get(STORES_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)

    def test_retrieve_only_verified_stores(self):
        """
        Test to ensure that only verified store will be retrieved,
        for unauthenticated users or those that doesnt own the store
        """

        smpl.sample_store(smpl.sample_user(), self.store_category, self.city)
        store2 = smpl.sample_store(smpl.sample_user(
            phone="+989123456788"), self.store_category, self.city, is_verified=True)

        res = self.client.get(detail_url(store2.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], store2.name)

    # Category
    def test_list_only_verfied_categories(self):
        """ Test only list verified categories  """
        smpl.sample_category(
            self.store_category, name="Shoes", is_verified=False)
        category2 = smpl.sample_category(
            self.store_category, name="Shirts", is_verified=True)

        res = self.client.get(CATEGORIES_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(category2.name, res.data["results"][0]["name"])

    def test_list_only_verified_sub_categories(self):
        """ Test to ensure that only verified categories will be listed  """

        category = smpl.sample_category(
            self.store_category, name="Shirts", is_verified=True)
        smpl.sample_sub_category(store_category=self.store_category,
                                 name="Sport shirts",
                                 is_verified=False,
                                 parent_category=category)
        sub_category2 = smpl.sample_sub_category(store_category=self.store_category,
                                                 name="Minimal Shirts",
                                                 is_verified=True,
                                                 parent_category=category)

        res = self.client.get(CATEGORIES_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(len(res.data["results"][0]["sub_categories"]), 1)
        self.assertEqual(
            res.data["results"][0]["sub_categories"][0]["name"], sub_category2.name)

    def test_retrieve_only_verfied_category(self):
        """ Test to ensure that only verified category will be retrieved  """
        category = smpl.sample_category(
            self.store_category, name="Shoes", is_verified=False)

        res = self.client.get(detail_url(category.id, "category"))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn("name", res.data)

    def test_list_products_by_category(self):
        """ Test list all products of a category """
        category = smpl.sample_category(
            self.store_category,
            is_verified=True,
            name="Sea food")

        store = smpl.sample_store(
            smpl.sample_user(), self.store_category, self.city)
        brand = smpl.sample_brand()
        smpl.sample_supermarket_product(category,
                                        store,
                                        is_verified=True)
        smpl.sample_supermarket_product(category,
                                        store,
                                        is_verified=True)
        smpl.sample_supermarket_product(category,
                                        store,
                                        is_verified=False)

        res = self.client.get(
            reverse("store:category-products", args=[category.id]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    # Brand
    def test_list_only_verified_brands(self):
        """ Test to ensure that only verified brands will be listed """
        smpl.sample_brand(name_fa="????????", name_en="Nike")
        brand2 = smpl.sample_brand(
            name_fa="????????????", name_en="Adidas", is_verified=True)
        res = self.client.get(BRAND_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["name_fa"], brand2.name_fa)
        self.assertEqual(res.data["results"][0]["name_en"], brand2.name_en)

    def test_retrieve_only_verified_brand(self):
        """ Test to ensure that only verified brand will be retrieved """

        brand = smpl.sample_brand(name_fa="????????????",
                                  name_en="Adidas",
                                  is_verified=False)
        res = self.client.get(detail_url(brand.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Supermarket Product
    def test_list_only_verified_supermarket_products(self):
        """ Test to ensure that only verified supermarket products will be listed """
        smpl.sample_supermarket_product(
            smpl.sample_category(
                self.store_category),
            smpl.sample_store(smpl.sample_user(), self.store_category,
                              self.city),
            is_verified=False)

        res = self.client.get(SUPERMARKET_PRODUCT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 0)

    def test_retrieve_only_verified_product(self):
        """ Test to ensure that only verified supermarket product will be retrieved """
        smpl.sample_supermarket_product(smpl.sample_category(
            self.store_category),
            smpl.sample_store(smpl.sample_user(), self.store_category,
                              self.city),
            is_verified=False)

        res = self.client.get(SUPERMARKET_PRODUCT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 0)


class StorePrivateApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = smpl.sample_user(phone_is_verified=True)

        self.user2 = smpl.sample_user(
            phone="+989123456788",
            phone_is_verified=True)

        self.unverified_user = smpl.sample_user(
            phone="+989123456787",
            phone_is_verified=False)

        self.store_category = smpl.sample_store_category()
        self.city = smpl.sample_city()
        self.client.force_authenticate(user=self.user)

    # Store
    def test_user_create_store(self):
        """
        Test to ensure that user is able to create
        new store.
        """

        payload = {
            "name": "HameMarketPirax",
            "address": "sdjlk2 ,3 j,xc9",
            "long": 32.612,
            "lat": 42.512,
            "city": self.city.id,
            "store_category": self.store_category.id
        }

        res = self.client.post(STORES_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])

    def test_store_owner_is_current_authenticated_user(self):
        """
        Test to ensure that user is able to create
        new store.
        """

        payload = {
            "name": "HameMarketPirax",
            "address": "sdjlk2 ,3 j,xc9",
            "long": 32.612,
            "lat": 42.512,
            "city": self.city.id,
            "store_category": self.store_category.id
        }

        res = self.client.post(STORES_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["owner"], self.user.id)

    def test_user_update_own_store(self):
        """ Test that user can only update their own store profile """
        user2 = smpl.sample_user("+989123456500")
        store = smpl.sample_store(
            user2, self.store_category, city=self.city, is_verified=True)

        payload = {"is_open": True}
        res = self.client.patch(detail_url(store.id), payload)

        store.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(store.is_open, False)

    def test_any_update_unverifies_the_store_except_is_open(self):
        """
        Test that any update to store makes is_verified to False
        so it needs to get verified again except is_open field
        """
        store = smpl.sample_store(
            self.user, self.store_category, self.city, is_verified=True)
        payload = {"is_open": True}

        self.assertTrue(store.is_verified)

        res = self.client.patch(detail_url(store.id), payload)
        store.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(store.is_verified)

        payload = {"description": "new description"}

        self.assertTrue(store.is_verified)

        res = self.client.patch(detail_url(store.id), payload)
        store.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(store.is_verified)

    def test_optionally_list_all_stores_that_user_owns(self):
        """
        Test if that user is authenticated, owns the store and
        parameter self=true is passed then list all stores that user owns
        """

        smpl.sample_store(self.user, self.store_category,
                          self.city,
                          is_verified=False)
        smpl.sample_store(self.user, self.store_category,
                          self.city,
                          is_verified=True)

        res = self.client.get(STORES_LIST_URL, {"self": "true"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    # Category
    def test_user_create_category(self):
        """
        Test create a category.
        a category must have a "store_category" field
        """

        payload = {
            "name": "Shoes",
            "store_category": self.store_category.id
        }

        res = self.client.post(CATEGORIES_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.data)
        self.assertIn("store_category", res.data)

    def test_user_create_sub_category(self):
        """
        Test create a sub category.
        a sub category must have a "store_category" and "parent_category" field
        """
        category = smpl.sample_category(
            self.store_category, is_verified=True)
        payload = {
            "name": "Shirts",
            "store_category": self.store_category.id,
            "parent_category": category.id

        }

        res = self.client.post(CATEGORIES_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.data)
        self.assertIn("store_category", res.data)
        self.assertIn("parent_category", res.data)

    def test_category_owner_is_current_authenticated_user(self):
        """
        Test owner of category is the authenticated user,
        that created it.
        """
        payload = {
            "name": "Shop",
            "store_category": self.store_category.id
        }

        res = self.client.post(CATEGORIES_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["owner"], self.user.id)

    def test_optionally_list_all_categories_that_user_owns(self):
        """
        Test if user is authenticated, owns the category,
        and parameter self=true then list all categories
        that user owns.
        """
        category1 = smpl.sample_category(
            self.store_category, name="Shoes", owner=self.user, is_verified=False)
        category2 = smpl.sample_category(
            self.store_category, name="Shirts", owner=self.user, is_verified=True)

        res = self.client.get(CATEGORIES_LIST_URL, {"self": "true"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    # Brand

    def test_user_create_brand(self):
        """ Ensure that user is able to create a brand """
        payload = {
            "name_fa": "????????",
            "name_en": "Nike"
        }

        res = self.client.post(BRAND_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name_fa"], payload["name_fa"])

    def test_brand_owner_is_current_authenticated_user(self):
        """
        Test the owner of brand is authenticated user,
        that created it
        """

        payload = {
            "name_fa": "????????",
            "name_en": "nike"
        }

        res = self.client.post(BRAND_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["owner"], self.user.id)

    def test_optionally_list_all_brands_that_user_owns(self):
        category = smpl.sample_category(self.store_category)
        brand1 = smpl.sample_brand(category=category,
                                   name_fa="????????",
                                   name_en="nike",
                                   owner=self.user)
        brand2 = smpl.sample_brand(category=category,
                                   name_fa="????????????",
                                   name_en="Adidas",
                                   owner=self.user)

        res = self.client.get(BRAND_LIST_URL, {"self": "true"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    # Supermarket Product
    def test_user_create_supermarket_product(self):
        """ Test create a supermarket product  """
        store = smpl.sample_store(
            self.user, self.store_category, self.city, is_verified=True)
        category_shoes = smpl.sample_category(self.store_category, "Food")
        brand_nike = smpl.sample_brand(
            category_shoes, "??????????????????", "Zar makaron")

        payload = {
            "name": "???????????????? ???????? ????",
            "sale_price": 10000,
            "stock": 500,
            "discount": 10,
            "in_bulk": True,
            "brand": brand_nike.id,
            "category": category_shoes.id,
            "store": store.id
        }

        res = self.client.post(SUPERMARKET_PRODUCT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("name", res.data)
        self.assertEqual(res.data["name"], payload["name"])

    def test_user_can_only_assign_own_store_on_create(self):
        """
        Test that user can only assign own store to the product on create
        """

        store2 = smpl.sample_store(
            self.user2, self.store_category, self.city, is_verified=True)
        category_shoes = smpl.sample_category(self.store_category, "Food")
        brand_nike = smpl.sample_brand(
            category_shoes, "??????????????????", "Zar makaron")

        payload = {
            "name": "???????????????? ???????? ????",
            "sale_price": 10000,
            "stock": 500,
            "discount": 10,
            "in_bulk": True,
            "brand": brand_nike.id,
            "category": category_shoes.id,
            "store": store2.id
        }

        res = self.client.post(SUPERMARKET_PRODUCT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("name", res.data)

    def test_user_can_only_update_own_products(self):
        """ Test user can only update own products """
        product = smpl.sample_supermarket_product(smpl.sample_category(
            self.store_category),
            smpl.sample_store(self.user2, self.store_category,
                              self.city),
            is_verified=True)

        payload = {
            "sale_price": 11000
        }

        res = self.client.patch(detail_url(
            product.id, "supermarket-product"), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(product.name, res.data)

    # WishList
    def test_user_add_product_to_wish_list(self):
        """ Test user is able to add a product to hes wish list """
        product = smpl.sample_supermarket_product(smpl.sample_category(
            self.store_category),
            smpl.sample_store(self.user2, self.store_category,
                              self.city),
            is_verified=True)

        payload = {
            "product": product.id
        }

        res = self.client.post(WISH_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["product"], product.id)


class ProductImageUploadTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = smpl.sample_user()

        self.client.force_authenticate(self.user)
        self.city = smpl.sample_city()
        self.store_category = smpl.sample_store_category("sa")
        self.store = smpl.sample_store(
            self.user, self.store_category, self.city)
        self.category = smpl.sample_category(self.store_category)
        self.product = smpl.sample_product(self.category, self.store)

    def tearDown(self) -> None:
        self.product.delete()

    def test_upload_image_for_a_product(self):
        """ Test uploading an image for product """

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            payload = {
                "image": ntf,
                "product": self.product.id
            }
            res = self.client.post(
                PRODUCT_IMAGE_UPLOAD_URL, payload, format="multipart")

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            self.assertIn("image", res.data)

    def test_upload_image_bad_request(self):
        """ Test uploading an invalid image """
        res = self.client.post(PRODUCT_IMAGE_UPLOAD_URL, {
                               "image": "notimage"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
