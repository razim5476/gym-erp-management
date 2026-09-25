"""
Docstring for accounts.serializers.minimal_serializers
"""


from rest_framework import serializers
from accounts.models import AccountGroups, Accounts, Bank, PaymentMethod, Tax



class MinimalAccountGroupSerialzier(serializers.ModelSerializer):
    """
    Docstring for MinimalAccountGroupSerialzier
    """

    class Meta:
        model = AccountGroups
        fields = [
            'group_id', 'name'
        ]



class MinimalAccountSerializer(serializers.ModelSerializer):
    """
    MinimalAccountSerializer
    """

    class Meta:
        model = Accounts
        fields = [
            'account_id', 'name'
        ]



class MinimalBankSerializer(serializers.ModelSerializer):
    """
    MinimalBankSerializer
    """

    class Meta:
        model = Bank
        fields= [
            'bank_id', 'name'
        ]



class MinimalTaxSerializer(serializers.ModelSerializer):
    """
    MinimalTaxSerializer
    """

    class Meta:
        model = Tax
        fields = [
            'tax_id', 'name'
        ]

        


class MinimalPaymentMethodSerializer(serializers.ModelSerializer):
    """
    MinimalPaymentMethodSerializer
    """

    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'payment_method_id', 'name', 'account'
        ]


