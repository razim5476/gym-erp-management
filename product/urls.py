"""
Product urls.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product.views import ProductCategoryDropdownViewSet, ProductCategoryViewSet

router = DefaultRouter()

router.register(
    r'product_category',
    ProductCategoryViewSet,
    basename='product_category'
)
router.register(
    r'product_category_dropdown',
    ProductCategoryDropdownViewSet,
    basename='product_category_dropdown'
)

urlpatterns = [
    path('', include(router.urls)),
]
