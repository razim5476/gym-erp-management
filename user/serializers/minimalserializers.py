"""
Docstring for user.serializers.minimalserializers
"""
from rest_framework import serializers
from user.models import Address, Permission, Role, User


class MinimalRoleSerializers(serializers.ModelSerializer):
    """
    MinimalRoleSerializers
    """

    class Meta:
        model = Role
        fields = [
            'role_id', 'name'
        ]


class MinimalPermissionSerializer(serializers.ModelSerializer):
    """
    MinimalPermissionSerializer
    """

    class Meta:
        model = Permission
        fields = [
            'permission_id', 'name', 'code'
        ]


class MinimalUserSerializer(serializers.ModelSerializer):
    """
    MinimalUserSerializer
    """

    class Meta:
        model = User
        fields = [
            'user_id', 'firstname'
        ]



class MinimalAddressSerializer(serializers.ModelSerializer):
    """
    MinimalAddressSerializer
    """

    class Meta:
        model = Address
        fields = [
            'address_id'
        ]


