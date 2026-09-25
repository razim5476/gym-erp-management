"""
Product views.
"""

from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import get_objects_for_user
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from core.permissions import constants
from core.permissions.base_permission import GuardianPermission
from core.views import CoreModelViewSet
from product.models import ProductCategory
from product.serializers.minimal_serializers import (
    MinimalProductCategorySerializer,
)
from product.serializers.serializers import ProductCategorySerializer


class ProductCategoryViewSet(CoreModelViewSet):
    """
    Product Category CRUD APIs.
    """

    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    search_fields = ['name', 'product_category_id', 'hsn_code']
    ordering_fields = ['name', 'created_at', 'updated_at']

    permission_map = {
        "list": constants.ProductCategoryPermissions.VIEW_PRODUCT_CATEGORY,
        "retrieve": constants.ProductCategoryPermissions.VIEW_PRODUCT_CATEGORY,
        "create": constants.ProductCategoryPermissions.CREATE_PRODUCT_CATEGORY,
        "update": constants.ProductCategoryPermissions.EDIT_PRODUCT_CATEGORY,
        "partial_update": (
            constants.ProductCategoryPermissions.EDIT_PRODUCT_CATEGORY
        ),
        "destroy": constants.ProductCategoryPermissions.DELETE_PRODUCT_CATEGORY,
        "product_category_soft_delete": (
            constants.ProductCategoryPermissions.DISABLE_PRODUCT_CATEGORY
        )
    }

    @action(
        url_name='product_category_soft_delete',
        methods=['POST'],
        url_path='product_category_soft_delete',
        detail=True
    )
    def product_category_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk,
            ProductCategory,
            constants.ProductCategoryPermissions.DISABLE_PRODUCT_CATEGORY,
            "product category"
        )


class ProductCategoryDropdownViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Product Category dropdown APIs.
    """

    serializer_class = MinimalProductCategorySerializer
    queryset = ProductCategory.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, GuardianPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'product_category_id']
    ordering_fields = ['name', 'created_at']
    permission_map = {
        "list": constants.ProductCategoryPermissions.VIEW_PRODUCT_CATEGORY,
        "retrieve": constants.ProductCategoryPermissions.VIEW_PRODUCT_CATEGORY,
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.order_by('name')

        return get_objects_for_user(
            user,
            constants.ProductCategoryPermissions.VIEW_PRODUCT_CATEGORY,
            klass=ProductCategory
        ).filter(is_active=True).order_by('name')
