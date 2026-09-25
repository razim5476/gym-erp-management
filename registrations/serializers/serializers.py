"""
Serializers for registrations app
"""
from rest_framework import serializers
from registrations.models import CustomerGroup, Customer, SupplierGroup, Supplier
from user.models import Address
from accounts.models import TaxGroups, Accounts
from user.serializers.minimalserializers import MinimalUserSerializer, MinimalAddressSerializer
from organization.serializers.minimalserializers import MinimalCompanySerializer, MinimalBranchSerializer
from accounts.serializers.minimal_serializers import MinimalTaxSerializer, MinimalAccountSerializer
from registrations.serializers.minimal_serializers import MinimalCustomerGroupSerializer, MinimalSupplierGroupSerializer

class CustomerGroupSerializer(serializers.ModelSerializer):
    """CustomerGroupSerializer"""
    company = MinimalCompanySerializer(read_only=True)
    branch = MinimalBranchSerializer(read_only=True)
    
    tax_group_id = serializers.PrimaryKeyRelatedField(
        source='tax_group',
        queryset=TaxGroups.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = CustomerGroup
        fields = [
            'id', 'customer_group_id', 'group_name', 'description', 
            'company', 'branch', 'tax_group', 'tax_group_id',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at', 'company', 'branch']


class CustomerSerializer(serializers.ModelSerializer):
    """CustomerSerializer"""
    customer_group = MinimalCustomerGroupSerializer(read_only=True)
    customer_group_id = serializers.PrimaryKeyRelatedField(
        source='customer_group',
        queryset=CustomerGroup.objects.all(),
        write_only=True
    )
    
    account = MinimalAccountSerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        source='account',
        queryset=Accounts.objects.all(),
        write_only=True
    )
    
    shipping_address = MinimalAddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        source='shipping_address',
        queryset=Address.objects.all(),
        write_only=True
    )
    
    tax_group_id = serializers.PrimaryKeyRelatedField(
        source='tax_group',
        queryset=TaxGroups.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'customer_name', 'phone_number',
            'customer_group', 'customer_group_id', 'tax_group', 'tax_group_id',
            'account', 'account_id', 'customer_type', 'website',
            'shipping_address', 'shipping_address_id', 'tax_number',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at']


class SupplierGroupSerializer(serializers.ModelSerializer):
    """SupplierGroupSerializer"""
    company = MinimalCompanySerializer(read_only=True)
    branch = MinimalBranchSerializer(read_only=True)
    
    tax_group_id = serializers.PrimaryKeyRelatedField(
        source='tax_group',
        queryset=TaxGroups.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = SupplierGroup
        fields = [
            'id', 'supplier_group_id', 'name', 'description', 
            'company', 'branch', 'tax_group', 'tax_group_id',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at', 'company', 'branch']


class SupplierSerializer(serializers.ModelSerializer):
    """SupplierSerializer"""
    supplier_group = MinimalSupplierGroupSerializer(read_only=True)
    supplier_group_id = serializers.PrimaryKeyRelatedField(
        source='supplier_group',
        queryset=SupplierGroup.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    
    address = MinimalAddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        source='address',
        queryset=Address.objects.all(),
        write_only=True
    )
    
    account = MinimalAccountSerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        source='account',
        queryset=Accounts.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Supplier
        fields = [
            'id', 'supplier_id', 'supplier_name', 'alias',
            'supplier_group', 'supplier_group_id', 'supplier_type', 'website',
            'address', 'address_id', 'tax_number', 'account', 'account_id',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at']
