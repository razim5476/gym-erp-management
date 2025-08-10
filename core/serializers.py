"""
Core Serilizers
"""
from rest_framework import serializers


class ReadOnlyFieldsSerializer(serializers.Serializer):
    """Serializer for the read_only fields.like created_at, updated_at, created_by, is_active"""

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
