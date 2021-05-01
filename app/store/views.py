from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.http import request, JsonResponse
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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

    @action(methods=["GET"], detail=True, url_path="products", url_name="products")
    def products(self, request, *args, **kwargs):
        """
        Returns all products of this category
        """
        context = {
            "request": self.request
        }

        category = self.get_object()

        # Since we have multiple serializer class for different products
        # we need to specify which serializer class to be used depends on
        # current category, store_category, e.g if store_category == "Clothing" then ClothingProductSerializer

        st_category_name = category.store_category.name
        if st_category_name == "Supermarket":
            products = models.SupermarketProduct.objects.filter(
                category=category, is_verified=True)
            ProductSerializer = serializers.SupermarketProductSerializer
        else:
            products = models.Product.objects.filter(
                category=category, is_verified=True)
            ProductSerializer = serializers.ProductSerializer

        # Implement pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = serializers.SupermarketProductSerializer(
                page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.SupermarketProductSerializer(
            products, many=True
        )
        return Response(serializer.data)


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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsStoreOwnerToUpdate]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "brand__name_fa", "brand__name_en"]
    ordering_fields = ["name"]
    queryset = models.SupermarketProduct.objects.filter(is_verified=True)

    def create(self, request, *args, **kwargs):
        """
        Current authenticated user must be the owner
        of store that passed with product data
        """
        store_id = self.request.data.get("store", False)

        if store_id:
            try:
                models.Store.objects.get(id=store_id,
                                         owner=self.request.user)
            except models.Store.DoesNotExist:
                return Response({"detail": "only stores that user owns"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class ProductImageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """ Endpoint to upload image for a product """
    serializer_class = serializers.ProductImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.ProductImage.objects.all()


class WishListItemViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """ Endpoint to add products to the wishlist """
    serializer_class = serializers.WishlistItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.WishListItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        