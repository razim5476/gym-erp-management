"""
Core Serializers
"""


import uuid

from rest_framework import serializers

from core.models import (
    Barcodes,
    Brand,
    Category,
    Country,
    Currency,
    FinancialYear,
    PaginationSize,
    State,
    SubCategory,
    UniqueId,
    UnitOfMeasure,
)
from organization.models import Branch
from organization.serializers.minimalserializers import MinimalBranchSerializer


class CountrySerializer(serializers.ModelSerializer):
    """
    Country Serializer.
    """

    class Meta:
        model = Country
        fields = [
            'country_id', 'name', 'is_active', 'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'country_id', 'is_active', 'created_at', 'updated_at'
        ]


class StateSerializer(serializers.ModelSerializer):
    """
    State Serializer.
    """

    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        source='country',
        queryset=Country.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = State
        fields = [
            'state_id', 'name', 'country', 'country_id', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'state_id', 'is_active', 'created_at', 'updated_at'
        ]


class CurrencySerializer(serializers.ModelSerializer):
    """
    Currency Serializer.
    """

    class Meta:
        model = Currency
        fields = [
            'currency_id', 'name', 'code', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'currency_id', 'is_active', 'created_at', 'updated_at'
        ]


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    """
    Unit Of Measure Serializer.
    """

    class Meta:
        model = UnitOfMeasure
        fields = [
            'uom_id', 'name', 'short_name', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'uom_id', 'is_active', 'created_at', 'updated_at'
        ]


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand Serializer.
    """

    class Meta:
        model = Brand
        fields = [
            'brand_id', 'name', 'description', 'company', 'branch',
            'is_active', 'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'company', 'branch', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'brand_id': {'required': False}
        }

    def create(self, validated_data):
        if not validated_data.get('brand_id'):
            validated_data['brand_id'] = (
                f"BRAND-{uuid.uuid4().hex[:10].upper()}"
            )

        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Serializer.
    """

    class Meta:
        model = Category
        fields = [
            'category_id', 'name', 'description', 'company', 'branch',
            'is_active', 'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'company', 'branch', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'category_id': {'required': False}
        }

    def create(self, validated_data):
        if not validated_data.get('category_id'):
            validated_data['category_id'] = (
                f"CAT-{uuid.uuid4().hex[:10].upper()}"
            )

        return super().create(validated_data)


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Sub Category Serializer.
    """

    class Meta:
        model = SubCategory
        fields = [
            'sub_category_id', 'name', 'category', 'description', 'company',
            'branch', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        read_only_fields = [
            'company', 'branch', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'sub_category_id': {'required': False}
        }

    def create(self, validated_data):
        if not validated_data.get('sub_category_id'):
            validated_data['sub_category_id'] = (
                f"SUB-CAT-{uuid.uuid4().hex[:10].upper()}"
            )

        return super().create(validated_data)


class BarcodesSerializer(serializers.ModelSerializer):
    """
    Barcode Serializer.
    """

    class Meta:
        model = Barcodes
        fields = [
            'barcode_id', 'name', 'code', 'description', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'barcode_id', 'is_active', 'created_at', 'updated_at'
        ]


class PaginationSizeSerializer(serializers.ModelSerializer):
    """
    Pagination Size Serializer.
    """

    class Meta:
        model = PaginationSize
        fields = [
            'pagination_id', 'data_per_page', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'pagination_id', 'is_active', 'created_at', 'updated_at'
        ]


class UniqueIdSerializer(serializers.ModelSerializer):
    """
    Unique Id Serializer.
    """

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = UniqueId
        fields = [
            'prefix', 'unique_id', 'model', 'branch', 'branch_id',
            'is_active', 'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'is_active', 'created_at', 'updated_at'
        ]


class FinancialYearSerializer(serializers.ModelSerializer):
    """
    Financial Year Serializer.
    """

    class Meta:
        model = FinancialYear
        fields = [
            'financial_year_id', 'start_date', 'end_date', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'financial_year_id', 'is_active', 'created_at', 'updated_at'
        ]
