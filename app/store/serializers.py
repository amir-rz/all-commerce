from rest_framework import serializers

from . import models


class StoreSerializer(serializers.ModelSerializer):
    store_score = serializers.DecimalField(
        max_digits=2, decimal_places=1, min_value=0, max_value=5, read_only=True)

    class Meta:
        model = models.Store
        fields = "__all__"
        read_only_fields = ["id", "is_verified", "owner"]


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["id", "is_verified",
                            "store_category", "parent_category", "owner"]


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"
        read_only_fields = ["id", "is_verified", "owner"]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        fields = "__all__"
        read_only_fields = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = "__all__"
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(min_value=1, max_value=100)
    product_score = serializers.DecimalField(
        max_digits=2, decimal_places=1, min_value=0, max_value=5, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"

    # def create(self, validated_data):
    #     print("Validated data--", validated_data)
    #     product_image_data = validated_data['product_images']
    #     del validated_data['product_images']

    #     product_item_obj = models.Product.objects.create(**validated_data)

    #     for product_image in product_image_data:
    #         models.ProductImage.objects.create(
    #             product=product_item_obj, **product_image)


class SupermarketProductSerializer(ProductSerializer):

    class Meta:
        model = models.SupermarketProduct
        fields = "__all__"
        read_only_fields = ["id", "is_verified", "product_score"]


class WishlistItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WishListItem
        fields = "__all__"
        read_only_fields = ["user","id"]
