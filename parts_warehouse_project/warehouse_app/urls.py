from django.urls import include, path
from rest_framework import routers

from .views import PartViewSet, PartSearchView, CategoryViewSet

app_name = "warehouse_app"

router = routers.DefaultRouter()
router.register(r"parts", PartViewSet, basename="parts")
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
    path("parts-search/", PartSearchView.as_view(), name="parts-search"),
]
