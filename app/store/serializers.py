from rest_framework import serializers
from . import models


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = "__all__"
        read_only_fields = ["id", "is_verified", "owner"]
