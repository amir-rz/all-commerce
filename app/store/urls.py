from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("stores", views.StoreViewSet)
router.register("categories", views.CategoryViewSet)
router.register("brands", views.BrandViewSet)
router.register("supermarket-products",
                views.SupermarketProductViewSet, "supermarket-product")
router.register("upload-product-image",
                views.ProductImageViewSet, "upload-product-image")
router.register("wish-lists", views.WishListItemViewSet,"wish-list-item")


app_name = "store"
urlpatterns = [
    path("", include(router.urls)),
]
