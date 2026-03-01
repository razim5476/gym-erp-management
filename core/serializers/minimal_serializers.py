"""
Docstring for core.serializers.minimal_serializers
"""


from core.models import Currency
from rest_framework import serializers



class MinimalCurrencySerializer(serializers.ModelSerializer):
    """
    Docstring for MinimalCurrencySerializer
    """

    class Meta:
        model = Currency
        fields= [
            'currency_id', 'name', 'code'
        ]

