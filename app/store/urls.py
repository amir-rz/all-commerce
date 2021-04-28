from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("stores", views.StoreViewSet)
router.register("categories", views.CategoryViewSet)
router.register("brands", views.BrandViewSet)
router.register("supermarket-products", views.SupermarketProductViewSet, "supermarket-product")


app_name = "store"
urlpatterns = [
    path("", include(router.urls)),
]
