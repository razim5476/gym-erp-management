"""
User serializers.
"""

from rest_framework import serializers

from user.models import Address, Role, User
from user.serializers.minimalserializers import (
    MinimalAddressSerializer,
    MinimalRoleSerializers,
)



class UserSerialzier(serializers.ModelSerializer):
    """
    Docstring for UserSerialzier
    """

    role = MinimalRoleSerializers(many=True, read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='role',
        queryset=Role.objects.filter(is_active=True),
        required=False, allow_null=True
    )

    address = MinimalAddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.filter(is_active=True),
        source='address',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'user_id', 'first_name', 'last_name', 'username',
            'date_of_birth', 'joined_date', 'image', 'userr_type',
            'is_trainer', 'height', 'weight', 'email', 'phone_number',
            'is_active', 'created_at', 'updated_at', 'address',
            'address_id', 'role', 'role_id', 'company', 'branch'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']



class LoginSerializer(serializers.Serializer):
    """
    LoginSerializer
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

