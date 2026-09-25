from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerGroupViewSet,
    CustomerViewSet,
    SupplierGroupViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register(r'customer-groups', CustomerGroupViewSet, basename='customer-group')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'supplier-groups', SupplierGroupViewSet, basename='supplier-group')
router.register(r'suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
