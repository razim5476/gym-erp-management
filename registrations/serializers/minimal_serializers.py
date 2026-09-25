"""
Minimal serializers for registrations app
"""
from rest_framework import serializers
from registrations.models import CustomerGroup, Customer, SupplierGroup, Supplier

class MinimalCustomerGroupSerializer(serializers.ModelSerializer):
    """MinimalCustomerGroupSerializer"""
    class Meta:
        model = CustomerGroup
        fields = ['id', 'customer_group_id', 'group_name']

class MinimalCustomerSerializer(serializers.ModelSerializer):
    """MinimalCustomerSerializer"""
    class Meta:
        model = Customer
        fields = ['id', 'customer_id', 'customer_name']

class MinimalSupplierGroupSerializer(serializers.ModelSerializer):
    """MinimalSupplierGroupSerializer"""
    class Meta:
        model = SupplierGroup
        fields = ['id', 'supplier_group_id', 'name']

class MinimalSupplierSerializer(serializers.ModelSerializer):
    """MinimalSupplierSerializer"""
    class Meta:
        model = Supplier
        fields = ['id', 'supplier_id', 'supplier_name']
