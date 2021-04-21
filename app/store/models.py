from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField

import csv


class Store(models.Model):
    """ 'Store' database model in the system """
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey("City", on_delete=models.SET_NULL, null=True)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    phone = PhoneNumberField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="name", unique=True, blank=True)

    def __str__(self):
        return self.name


class City(models.Model):
    """ City database model in the system """
    name = models.CharField(max_length=255, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name
