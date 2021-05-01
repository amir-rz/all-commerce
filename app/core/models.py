from django.db import models


class StoreCategory(models.Model):
    """ Website core categories database model in the system """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Store categories"