from django.db import models
from django.conf import settings
from django.utils.text import slugify

from autoslug import AutoSlugField


class Store(models.Model):
    """ 'Store' database model in the system """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey("City", on_delete=models.SET_NULL, null=True)
    long = models.DecimalField(max_digits=8, decimal_places=6)
    lat = models.DecimalField(max_digits=8, decimal_places=6)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    store_score = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, default=None)
    is_open = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class City(models.Model):
    """ City database model in the system """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Category database model in the system """
    name = models.CharField(max_length=255, unique=True)
    website_category = models.ForeignKey(
        "core.WebsiteCategory", on_delete=models.CASCADE)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Brand database model in the system """
    name_fa = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name_en = self.name_en.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.name_en:
            return f"{self.name_fa} - {self.name_en}"

        return self.name_fa


class Product(models.Model):
    """ Product database model in the system """
    name = models.CharField(max_length=255)
    # "000, fff" comma serprated hex codes
    colors = models.CharField(max_length=500)
    purchased_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    weight_in_grams = models.IntegerField(default=0, blank=True)
    in_bulk = models.BooleanField(default=False)
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
