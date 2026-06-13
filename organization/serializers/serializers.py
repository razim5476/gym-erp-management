"""
Organization serializers
"""


from rest_framework import serializers
from core.utils import generate_id, generate_unique_id
from organization.models import Branch, BranchSettings, BranchTrainers, BranchWorkingTimeAndDays, Company, CompanySettings, Warehouse
from organization.serializers.minimalserializers import MinimalBranchSerializer
from user.serializers.minimalserializers import MinimalUserSerializer


class CompanySerializer(serializers.ModelSerializer):
    """
    Company Serializer.
    """

    updated_by = MinimalUserSerializer(read_only=True)
    created_by = MinimalUserSerializer(read_only=True)


    class Meta:
        model = Company
        fields = [
            'company_id', 'name', 'short_name', 'webiste', 'build_date', 'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'company_id', 'updated_by', 'created_by', 'updated_at', 'created_at'
        ]



class CompanySettingsSerializer(serializers.ModelSerializer):
    """
    Company settings serializer.
    """

    owner_status = serializers.ChoiceField(choices=CompanySettings.OWNER_STATUS)

    class Meta:
        model = CompanySettings
        fields = [
            'address', 'financial_year', 'logo', 'language', 'owner_type', 'owner_status',
            'gstin_number', 'currency', 'updated_by', 'created_by', 'updated_at', 'created_at'
        ]




class CombinedCompanyCreateSerializer(serializers.Serializer):
    """
    Company and Company Settings combined serializer.
    """

    company_serializer = CompanySerializer(write_only=True)
    company_settings_serializer = CompanySettingsSerializer(write_only=True)


    def create(self, validated_data):
        
        company_data = validated_data.pop("company_serializer")
        company_settings_data = validated_data.pop("company_settings_serializer")


        request = self.context.get("request")
        user = request.user if request else None

        company_obj = Company.objects.create(
            company_id=generate_id(),
            **company_data,
            created_by=user
        )

        company_settings_obj = CompanySettings.objects.create(
            company=company_obj,
            **company_settings_data,
            created_by=user
        )

        return {
            "company": company_obj,
            "company_settings": company_settings_obj
        }

    def to_representation(self, instance):
        return {
            "company": CompanySerializer(instance["company"]).data,
            "company_settings": CompanySettingsSerializer(instance["company_settings"]).data
        }



class BranchSerializer(serializers.ModelSerializer):
    """
    Branch Serializer
    """

    class Meta:
        model = Branch
        fields = [
            'branch_id', 'name', 'short_name', 'website', 'buidl_date', 'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'branch_id', 'updated_by', 'created_by', 'updated_at', 'created_at'
        ]



class BranchSettingsSerializer(serializers.Serializer):
    """
    Branch Settings Serializer.
    """

    class Meta:
        model = BranchSettings
        fields = [
            'company', 'address', 'trainers', 'is_unisex', 'type', 'phone_number', 'created_by', 'created_at', 'updated_by', 'updated_at'
        ]
        read_only_fields = [
           'created_by', 'created_at', 'updated_by', 'updated_at'
        ]



class CombinedBranchCreateSerializer(serializers.Serializer):
    """
    Combined Branch and Branch Settings
    """

    branch_serializer = BranchSerializer(write_only=True)
    branch_settings_serializer = BranchSettingsSerializer(write_only=True)


    def create(self, validated_data):
        

        branch_data = validated_data.data('branch_serializer')
        branch_settings_data = validated_data.data('branch_settings_serializer')


        request = self.context.get('request')
        user = request.user if request else None

        branch_obj = Branch.objects.create(
            branch_id=generate_id(),
            created_by=request.user,
            **branch_data
        )

        branch_settings_obj = BranchSettings.objects.create(
            branch=branch_obj,
            **branch_settings_data
        )

        return {
            'branch': branch_obj,
            'branch_settings': branch_settings_obj
        }
    
    def to_representation(self, instance):
        return {
            "branch": BranchSerializer(instance["branch"]).data,
            "branch_settings": BranchSettingsSerializer(instance["branch_settings"]).data
        }
    


class BranchTrainerSerializer(serializers.ModelSerializer):
    """
    Branch Trainer Serializer.
    """

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Branch.objects.filter(is_active=True),
        source='branch'
    )
    trainer = serializers.IntegerField(
        help_text='Store the primary of the trainer.'
    )

    class Meta:
        model = BranchTrainers
        fields = [
            'branch', 'branch_id', 'trainer'
        ]



class BranchWorkingTimeAndDaysSerializer(serializers.ModelSerializer):
    """
    Branch Working Time and Days Serializer
    """

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True
    )

    class Meta:
        model = BranchWorkingTimeAndDays
        fields = [
            'branch', 'branch_id', 'am_from', 'am_to', 'pm_from', 'pm_to','ladies_time', 'mixed_time',
            'working_days', 'is_holidays'
        ]



class WarehouseSerializer(serializers.ModelSerializer):
    """
    Warehouse Serializer
    """

    branch = MinimalBranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.filter(is_active=True),
        source='branch',
        write_only=True
    )
    address = serializers.IntegerField(
        help_text='Store the address primary key.'
    )
    account = serializers.IntegerField(
        help_text='Store the account primary key.'
    )

    class Meta:
        model = Warehouse
        fields = [
            'warehouse_id', 'name', 'is_return_warehouse', 'company', 'branch', 'branch_id',
            'address', 'account'
        ]


    