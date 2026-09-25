"""
Product.Minimal Serializers
"""

from rest_framework import serializers
from product.models import ProductCategory



class MinimalProductCategorySerializer(serializers.ModelSerializer):
    """
    Minimal Product Category Serializer.
    """

    class Meta:
        model = ProductCategory
        fields = [
            'id', 'product_category_id', 'name'
        ]


