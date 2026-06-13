"""
Core urls
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BarcodesViewSet,
    BrandViewSet,
    CategoryViewSet,
    CountryViewSet,
    CurrencyViewSet,
    FinancialYearViewSet,
    PaginationSizeViewSet,
    StateViewSet,
    SubCategoryViewSet,
    UniqueIdViewSet,
    UnitOfMeasureViewSet,
)

router = DefaultRouter()

router.register(r'country', CountryViewSet, basename='country')
router.register(r'state', StateViewSet, basename='state')
router.register(r'currency', CurrencyViewSet, basename='currency')
router.register(
    r'unit_of_measure',
    UnitOfMeasureViewSet,
    basename='unit_of_measure'
)
router.register(r'brand', BrandViewSet, basename='brand')
router.register(r'category', CategoryViewSet, basename='category')
router.register(
    r'sub_category',
    SubCategoryViewSet,
    basename='sub_category'
)
router.register(r'barcode', BarcodesViewSet, basename='barcode')
router.register(
    r'pagination_size',
    PaginationSizeViewSet,
    basename='pagination_size'
)
router.register(r'unique_id', UniqueIdViewSet, basename='unique_id')
router.register(
    r'financial_year',
    FinancialYearViewSet,
    basename='financial_year'
)


urlpatterns = [
    path('', include(router.urls)),
]
