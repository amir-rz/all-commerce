from django.test import TestCase


from .. import models


class ModelsTests(TestCase):

    def test_website_category_str_repr(self):
        """ Test website category string representation """
        website_category = models.WebsiteCategory.objects.create(
            name="Food"
        )

        self.assertEqual(str(website_category), website_category.name)
