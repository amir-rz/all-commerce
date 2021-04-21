from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework import permissions

from . import serializers
from . import models

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Store.objects.all()
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
