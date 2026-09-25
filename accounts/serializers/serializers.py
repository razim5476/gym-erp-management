"""
Docstring for accounts.serializers.serializers
"""


from rest_framework import serializers

from accounts.models import AccountGroups, Accounts, Bank, BankBranch, BankAccount, PaymentMethod, Tax, TaxGroups
from accounts.serializers.minimal_serializers import MinimalAccountGroupSerialzier, MinimalAccountSerializer, MinimalBankSerializer, MinimalTaxSerializer
from core.models import Currency
from core.serializers.minimal_serializers import MinimalCurrencySerializer
from organization.models import Branch
from organization.serializers.minimalserializers import MinimalCompanySerializer, MinimalBranchSerializer
from user.models import Address
from user.serializers.minimalserializers import MinimalAddressSerializer, MinimalUserSerializer



class AccountGroupSerializer(serializers.ModelSerializer):
    """
    Docstring for AccountGroupSerializer
    """

    created_by = MinimalUserSerializer(read_only=True)
    company = MinimalCompanySerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)

    root_type = serializers.ChoiceField(choices=AccountGroups.ACCOUNT_GROUP_TYPES)

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = AccountGroups
        fields = [
            'group_id', 'name', 'parent', 'level', 'root_type', 'company', 
            'branch_id', 'branch', 'created_by', 'updated_by', 'is_active'
        ]
        read_only_fields = [
            'is_active', 'updated_by', 'group_id'
        ]


class AccountSerializer(serializers.ModelSerializer):
    """
    AccountSerializer
    """

    currency = MinimalCurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        source='currency',
        write_only=True,
        queryset=Currency.objects.filter(is_active=True)
    )

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source='branch',
        queryset=Branch.objects.filter(is_active=True),
        write_only=True
    )

    account_group = MinimalAccountGroupSerialzier(read_only=True)
    account_group_id = serializers.PrimaryKeyRelatedField(
        source='account_group',
        queryset=AccountGroups.objects.filter(is_active=True),
        write_only=True
    )

    sub_type = serializers.ChoiceField(choices=Accounts.ACCOUNT_SUB_TYPES)
    created_by = MinimalUserSerializer(read_only=True)
    company = MinimalCompanySerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Accounts
        fields = [
            'account_id', 'name', 'account_group_id', 'account_group', 'currency_id',
            'currency', 'sub_type', 'company', 'branch', 'branch_id',  'is_active', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'is_active'
        ]


class BankSerializer(serializers.ModelSerializer):
    """
    BankSerializer
    """

    class Meta:
        model = Bank
        fields = [
            'bank_id', 'name', 'swift_code'
        ]



class BankBranchSerializer(serializers.ModelSerializer):
    """
    BankBranchSerializer
    """

    created_by = MinimalUserSerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)

    address_id = serializers.PrimaryKeyRelatedField(
        source='address',
        queryset=Address.objects.filter(is_active=True),
        write_only=True
    )
    address = MinimalAddressSerializer(read_only=True)

    class Meta:
        model = BankBranch
        fields = [
            'bank_branch_id', 'bank', 'bank_id', 'name', 'swift_code',
            'address_id', 'address', 'created_by', 'updated_by', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'is_active', 'created_at', 'updated_at'
        ]



class BankAccountSerializer(serializers.ModelSerializer):
    """
    BankAccount
    """

    bank_branch = MinimalBankSerializer(read_only=True)
    bank_branch_id = serializers.PrimaryKeyRelatedField(
        source='bank_branch',
        write_only=True,
        queryset=BankBranch.objects.filter(is_active=True)
    )

    account = MinimalAccountSerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Accounts.objects.filter(is_active=True),
        source='account',
        write_only=True
    )

    account_type = serializers.ChoiceField(choices=BankAccount.ACCOUNT_TYPE)

    company = MinimalCompanySerializer(read_only=True)

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True
    )

    class Meta:
        model = BankAccount
        fields = [
            'bank_account_id', 'bank_branch', 'bank_branch_id', 'account', 'account_id', 'account_no', 'account_type', 
            'company', 'branch', 'contact_name', 'contact_no', 'is_default',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            ''
        ]



class TaxSerializer(serializers.ModelSerializer):
    """
    TaxSerializer
    """

    company = MinimalCompanySerializer(read_only=True)

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True
    )

    created_by = MinimalUserSerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Tax
        fields = [
            'tax_id', 'name', 'company', 'branch', 'branch_id', 'description', 'is_active', 'created_by', 'created_at', 'updated_by', 'updated_at'
        ]
        read_only_fields = [
            'is_active', 'created_at', 'updated_at'
        ]



class TaxGroupSerializer(serializers.ModelSerializer):
    """
    TaxGroupSerializer
    """

    tax = MinimalTaxSerializer(read_only=True)
    tax_id = serializers.PrimaryKeyRelatedField(
        queryset=Tax.objects.filter(is_active=True),
        source='tax',
        write_only=True
    )

    company = MinimalCompanySerializer(read_only=True)

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True
    )

    created_by = MinimalUserSerializer(read_only=True)

    updated_by = MinimalUserSerializer(read_only=True)


    class Meta:
        model = TaxGroups
        fields = [
            'tax_group_id', 'name', 'tax', 'tax_id', 'company', 'branch', 'branch_id', 'tax_rate', 'description', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'is_active', 'created_at', 'updated_at'
        ]




class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Payment Method Serializer.
    """

    account = MinimalAccountSerializer()
    created_by = MinimalUserSerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)
    branch = MinimalBranchSerializer(read_only=True)
    company = MinimalCompanySerializer(read_only=True)

    class Meta:
        model = PaymentMethod
        fields = [
            'payment_method_id', 'name', 'account', 'description', 'is_default',
            'company', 'branch', 'created_by', 'updated_by', 'created_at', 'updated_at',
            'is_active'
        ]





