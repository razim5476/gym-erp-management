"""
Views for registrations app
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, assign_perm
from core.views import StandardPageNumberPagination
from core.permissions.base_permission import GuardianPermission
from core.permissions import constants
from .models import CustomerGroup, Customer, SupplierGroup, Supplier
from .serializers import (
    CustomerGroupSerializer,
    CustomerSerializer,
    SupplierGroupSerializer,
    SupplierSerializer,
)

class CustomerGroupViewSet(viewsets.ModelViewSet):
    """CustomerGroupViewSet"""
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]

    permission_map = {
        "list": constants.CustomerGroupPermissions.VIEW_CUSTOMER_GROUP,
        "retrieve": constants.CustomerGroupPermissions.VIEW_CUSTOMER_GROUP,
        "create": constants.CustomerGroupPermissions.CREATE_CUSTOMER_GROUP,
        "update": constants.CustomerGroupPermissions.EDIT_CUSTOMER_GROUP,
        "partial_update": constants.CustomerGroupPermissions.EDIT_CUSTOMER_GROUP,
        "destroy": constants.CustomerGroupPermissions.DELETE_CUSTOMER_GROUP,
        "soft_delete": constants.CustomerGroupPermissions.DISABLE_CUSTOMER_GROUP
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomerGroup.objects.all()
        return get_objects_for_user(
            user,
            constants.CustomerGroupPermissions.VIEW_CUSTOMER_GROUP,
            klass=CustomerGroup
        ).filter(company=user.company, branch=user.branch)
        
    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(
            company=user.company, 
            branch=user.branch,
            created_by=user
        )
        assign_perm(constants.CustomerGroupPermissions.VIEW_CUSTOMER_GROUP, user, obj)
        assign_perm(constants.CustomerGroupPermissions.EDIT_CUSTOMER_GROUP, user, obj)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    @action(detail=True, methods=['post'], url_path='soft_delete', url_name='soft_delete')
    def soft_delete(self, request, pk=None):
        user = self.request.user
        obj = self.get_object()
        
        if not user.has_perm(constants.CustomerGroupPermissions.DISABLE_CUSTOMER_GROUP, obj):
            raise PermissionDenied("You don't have permission to disable this customer group.")
            
        obj.is_active = False
        obj.save()
        return Response({"message": "Customer Group disabled successfully."}, status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ModelViewSet):
    """CustomerViewSet"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]

    permission_map = {
        "list": constants.CustomerPermissions.VIEW_CUSTOMER,
        "retrieve": constants.CustomerPermissions.VIEW_CUSTOMER,
        "create": constants.CustomerPermissions.CREATE_CUSTOMER,
        "update": constants.CustomerPermissions.EDIT_CUSTOMER,
        "partial_update": constants.CustomerPermissions.EDIT_CUSTOMER,
        "destroy": constants.CustomerPermissions.DELETE_CUSTOMER,
        "soft_delete": constants.CustomerPermissions.DISABLE_CUSTOMER
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Customer.objects.all()
        return get_objects_for_user(
            user,
            constants.CustomerPermissions.VIEW_CUSTOMER,
            klass=Customer
        ).filter(customer_group__company=user.company, customer_group__branch=user.branch)

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(created_by=user)
        assign_perm(constants.CustomerPermissions.VIEW_CUSTOMER, user, obj)
        assign_perm(constants.CustomerPermissions.EDIT_CUSTOMER, user, obj)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    @action(detail=True, methods=['post'], url_path='soft_delete', url_name='soft_delete')
    def soft_delete(self, request, pk=None):
        user = self.request.user
        obj = self.get_object()
        
        if not user.has_perm(constants.CustomerPermissions.DISABLE_CUSTOMER, obj):
            raise PermissionDenied("You don't have permission to disable this customer.")
            
        obj.is_active = False
        obj.save()
        return Response({"message": "Customer disabled successfully."}, status=status.HTTP_200_OK)


class SupplierGroupViewSet(viewsets.ModelViewSet):
    """SupplierGroupViewSet"""
    queryset = SupplierGroup.objects.all()
    serializer_class = SupplierGroupSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]

    permission_map = {
        "list": constants.SupplierGroupPermissions.VIEW_SUPPLIER_GROUP,
        "retrieve": constants.SupplierGroupPermissions.VIEW_SUPPLIER_GROUP,
        "create": constants.SupplierGroupPermissions.CREATE_SUPPLIER_GROUP,
        "update": constants.SupplierGroupPermissions.EDIT_SUPPLIER_GROUP,
        "partial_update": constants.SupplierGroupPermissions.EDIT_SUPPLIER_GROUP,
        "destroy": constants.SupplierGroupPermissions.DELETE_SUPPLIER_GROUP,
        "soft_delete": constants.SupplierGroupPermissions.DISABLE_SUPPLIER_GROUP
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SupplierGroup.objects.all()
        return get_objects_for_user(
            user,
            constants.SupplierGroupPermissions.VIEW_SUPPLIER_GROUP,
            klass=SupplierGroup
        ).filter(company=user.company, branch=user.branch)
        
    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(
            company=user.company, 
            branch=user.branch,
            created_by=user
        )
        assign_perm(constants.SupplierGroupPermissions.VIEW_SUPPLIER_GROUP, user, obj)
        assign_perm(constants.SupplierGroupPermissions.EDIT_SUPPLIER_GROUP, user, obj)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    @action(detail=True, methods=['post'], url_path='soft_delete', url_name='soft_delete')
    def soft_delete(self, request, pk=None):
        user = self.request.user
        obj = self.get_object()
        
        if not user.has_perm(constants.SupplierGroupPermissions.DISABLE_SUPPLIER_GROUP, obj):
            raise PermissionDenied("You don't have permission to disable this supplier group.")
            
        obj.is_active = False
        obj.save()
        return Response({"message": "Supplier Group disabled successfully."}, status=status.HTTP_200_OK)


class SupplierViewSet(viewsets.ModelViewSet):
    """SupplierViewSet"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]

    permission_map = {
        "list": constants.SupplierPermissions.VIEW_SUPPLIER,
        "retrieve": constants.SupplierPermissions.VIEW_SUPPLIER,
        "create": constants.SupplierPermissions.CREATE_SUPPLIER,
        "update": constants.SupplierPermissions.EDIT_SUPPLIER,
        "partial_update": constants.SupplierPermissions.EDIT_SUPPLIER,
        "destroy": constants.SupplierPermissions.DELETE_SUPPLIER,
        "soft_delete": constants.SupplierPermissions.DISABLE_SUPPLIER
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Supplier.objects.all()
        return get_objects_for_user(
            user,
            constants.SupplierPermissions.VIEW_SUPPLIER,
            klass=Supplier
        ).filter(supplier_group__company=user.company, supplier_group__branch=user.branch)

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(created_by=user)
        assign_perm(constants.SupplierPermissions.VIEW_SUPPLIER, user, obj)
        assign_perm(constants.SupplierPermissions.EDIT_SUPPLIER, user, obj)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    @action(detail=True, methods=['post'], url_path='soft_delete', url_name='soft_delete')
    def soft_delete(self, request, pk=None):
        user = self.request.user
        obj = self.get_object()
        
        if not user.has_perm(constants.SupplierPermissions.DISABLE_SUPPLIER, obj):
            raise PermissionDenied("You don't have permission to disable this supplier.")
            
        obj.is_active = False
        obj.save()
        return Response({"message": "Supplier disabled successfully."}, status=status.HTTP_200_OK)
