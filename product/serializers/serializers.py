"""
Product.Serializers
"""

import uuid

from rest_framework import serializers

from product.models import ProductCategory
from product.serializers.minimal_serializers import (
    MinimalProductCategorySerializer,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Product Category Serializer.
    """

    parent = MinimalProductCategorySerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=ProductCategory.objects.filter(is_active=True),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = ProductCategory
        fields = [
            'id', 'product_category_id', 'name', 'tax_group', 'parent',
            'parent_id', 'hsn_code', 'is_group', 'description', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'product_category_id': {'required': False}
        }

    def create(self, validated_data):
        if not validated_data.get('product_category_id'):
            validated_data['product_category_id'] = (
                f"PROD-CAT-{uuid.uuid4().hex[:10].upper()}"
            )

        return super().create(validated_data)

