from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import models, serializers
from .permissions import IsOwnerOrReadOnly, IsStoreOwnerToUpdate


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name", "score", "is_open"]
    order = "score"
    search_fields = ["name"]
    queryset = models.Store.objects.filter(is_verified=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        list_of_data_keys = list(self.request.data.keys())
        if list_of_data_keys[0] == "is_open" and len(list_of_data_keys) == 1:
            serializer.save()
        else:
            serializer.save(is_verified=False)

    def get_queryset(self):
        _self = self.request.query_params.get("self")

        if _self == "true" and self.request.user.is_authenticated:
            return models.Store.objects.filter(owner=self.request.user)

        return super().get_queryset()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    serializer_class = serializers.CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    queryset = models.Category.objects.prefetch_related(Prefetch(
        "sub_categories",
        queryset=models.Category.objects.filter(is_verified=True))).filter(is_verified=True, parent_category=None)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        _self = self.request.query_params.get("self")
        if _self == "true" and self.request.user.is_authenticated:
            return models.Category.objects.prefetch_related(
                Prefetch("sub_categories",
                         queryset=models.Category.objects.filter(owner=self.request.user))).filter(owner=self.request.user)
        if self.action == "retrieve":
            return models.Category.objects.prefetch_related(
                Prefetch("sub_categories",
                         queryset=models.Category.objects.filter(is_verified=True))).filter(is_verified=True)
        return super().get_queryset()


class BrandViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    serializer_class = serializers.BrandSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name_fa", "name_en"]
    ordering_fields = ["name_fa", "name_en"]
    queryset = models.Brand.objects.filter(is_verified=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        _self = self.request.query_params.get("self")

        if _self == "true" and self.request.user.is_authenticated:
            return models.Brand.objects.filter(owner=self.request.user)

        return super().get_queryset()


class SupermarketProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SupermarketProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "brand__name_fa", "brand__name_en"]
    ordering_fields = ["name"]
    queryset = models.SupermarketProduct.objects.filter(is_verified=True)

    # def perform_create(self, serializer):
    #     store_id = self.request.data["store"]

    #     try:
    #         models.Store.objects.get(id=store_id,
    #                                  owner=self.request.user)
    #     except models.Store.DoesNotExist:
    #         raise ValidationError("Only store owner")
