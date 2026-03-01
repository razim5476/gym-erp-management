"""
User serializers.
"""

from rest_framework import serializers

from organization.models import Branch
from user.models import Role, User
from user.serializers.minimalserializers import MinimalRoleSerializers



class UserSerialzier(serializers.ModelSerializer):
    """
    Docstring for UserSerialzier
    """

    role = MinimalRoleSerializers(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='role',
        queryset=Role.objects.filter(is_active=True),
        required=False, allow_null=True
    )

    company = CompanyMinimalSerializer(read_only=True)
    branch = BranchMinimalSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True,
        required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'user_id', 'firstname', 'lastname', 'age', 'joined_date', 'image', 'userr_type', 'is_trainer', 'height', 'weight', 'email', 'phone_number', 'is_active', 'created_at', 'updated_at', 'address', 'address_id', 'role', 'role_id',
            'company', 'branch'
        ]