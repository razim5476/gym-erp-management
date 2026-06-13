"""
Docstring for core.serializers.minimal_serializers
"""


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


class MinimalCountrySerializer(serializers.ModelSerializer):
    """
    Minimal Country Serializer.
    """

    class Meta:
        model = Country
        fields = [
            'country_id', 'name'
        ]


class MinimalStateSerializer(serializers.ModelSerializer):
    """
    Minimal State Serializer.
    """

    country = MinimalCountrySerializer(read_only=True)

    class Meta:
        model = State
        fields = [
            'state_id', 'name', 'country'
        ]


class MinimalCurrencySerializer(serializers.ModelSerializer):
    """
    Minimal Currency Serializer.
    """

    class Meta:
        model = Currency
        fields = [
            'currency_id', 'name', 'code'
        ]


class MinimalUnitOfMeasureSerializer(serializers.ModelSerializer):
    """
    Minimal Unit Of Measure Serializer.
    """

    class Meta:
        model = UnitOfMeasure
        fields = [
            'uom_id', 'name', 'short_name'
        ]


class MinimalBrandSerializer(serializers.ModelSerializer):
    """
    Minimal Brand Serializer.
    """

    class Meta:
        model = Brand
        fields = [
            'brand_id', 'name'
        ]


class MinimalCategorySerializer(serializers.ModelSerializer):
    """
    Minimal Category Serializer.
    """

    class Meta:
        model = Category
        fields = [
            'category_id', 'name'
        ]


class MinimalSubCategorySerializer(serializers.ModelSerializer):
    """
    Minimal Sub Category Serializer.
    """

    class Meta:
        model = SubCategory
        fields = [
            'sub_category_id', 'name', 'category'
        ]


class MinimalBarcodesSerializer(serializers.ModelSerializer):
    """
    Minimal Barcode Serializer.
    """

    class Meta:
        model = Barcodes
        fields = [
            'barcode_id', 'name', 'code'
        ]


class MinimalPaginationSizeSerializer(serializers.ModelSerializer):
    """
    Minimal Pagination Size Serializer.
    """

    class Meta:
        model = PaginationSize
        fields = [
            'pagination_id', 'data_per_page'
        ]


class MinimalUniqueIdSerializer(serializers.ModelSerializer):
    """
    Minimal Unique Id Serializer.
    """

    class Meta:
        model = UniqueId
        fields = [
            'prefix', 'unique_id', 'model', 'branch'
        ]


class MinimalFinancialYearSerializer(serializers.ModelSerializer):
    """
    Minimal Financial Year Serializer.
    """

    class Meta:
        model = FinancialYear
        fields = [
            'financial_year_id', 'start_date', 'end_date'
        ]
