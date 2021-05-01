import os
import uuid

from django.conf import settings
from django.db import models
from django_jalali.db import models as jmodels
from autoslug.fields import AutoSlugField


def product_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/product/", filename)


class Store(models.Model):
    """ 'Store' database model in the system """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    long = models.DecimalField(max_digits=8, decimal_places=6)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    store_score = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, default=None, blank=True)

    city = models.ForeignKey("City", on_delete=models.CASCADE)
    store_category = models.ForeignKey(
        "core.StoreCategory", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name="stores")

    is_open = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    """ City database model in the system """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Category(models.Model):
    """ 
    Category database model in the system.
    if "parent_category" is passed then this is a subcategory
    """
    name = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    store_category = models.ForeignKey(
        "core.StoreCategory", on_delete=models.CASCADE)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_categories")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    """ Brand database model in the system """
    name_fa = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255, unique=True, blank=True)

    is_verified = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, null=True)
    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_en = self.name_en.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name_fa


class Product(models.Model):
    """ Product database model in the system """
    name = models.CharField(max_length=255)
    purchased_price = models.IntegerField(null=True, blank=True)
    sale_price = models.IntegerField()
    stock = models.PositiveIntegerField()
    product_score = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, default=None, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    brand = models.ForeignKey(
        "Brand", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    store = models.ForeignKey("Store", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="name", default="")
    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to=product_image_file_path)
    is_featured = models.BooleanField(default=False)
    created = jmodels.jDateField(auto_now_add=True)
    updated = jmodels.jDateField(auto_now=True)

    def __str__(self):
        return self.product.name


class SupermarketProduct(Product):
    """ Super market product database model in the system """

    weight_in_grams = models.IntegerField(default=0, blank=True)
    in_bulk = models.BooleanField(default=False)


class WishListItem(models.Model):
    """ Wish list database model in the system """
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    