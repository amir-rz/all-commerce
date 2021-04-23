from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from . import serializers
from . import models


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name", "score", "is_open"]
    search_fields = ["name"]
    queryset = models.Store.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_verified=False)
