from django.test import TestCase

from .. import models


class ModelsTests(TestCase):

    def test_store_category_str_repr(self):
        """ Test store category string representation """
        store_category = models.StoreCategory.objects.create(
            name="Food"
        )

        self.assertEqual(str(store_category), store_category.name)
