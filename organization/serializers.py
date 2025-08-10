"""
Serializer for the organizaiton app models.
"""
from rest_framework.response import Response
from rest_framework import serializers
from core.models import Country, State
from user.models import Trainer
from organization.models import Branch, BranchSettings
from django.db import transaction
from core.serializers import ReadOnlyFieldsSerializer


class BranchSerializer(ReadOnlyFieldsSerializer, serializers.ModelSerializer):
    """Branch serializer"""

    country = serializers.CharField(source="country.name", read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        source="country",
        queryset=Country.objects.filter(is_active=True),
        write_only=True
    )

    state = serializers.CharField(source="country.name", read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        source="state",
        queryset=State.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = Branch
        fields = [
            'name', 'place', 'city', 'country', 'country_id', 'state', 'state_id', 'location', 'address_line', 'address_line_2', 'address_line_3', 'pincode', 'created_at', 'updated_at', 'created_by', 'is_active'
        ]


class BranchSettingsSerializer(ReadOnlyFieldsSerializer, serializers.ModelSerializer):
    """Serializer for the branch settings."""

    branch = serializers.CharField(source="branch.name", read_only=True)

    trainers = serializers.CharField(source="trainers.name", write_only=True)
    trainers_id = serializers.PrimaryKeyRelatedField(
        source='trainers',
        write_only=True,
        queryset=Trainer.objects.filter(is_active=True)
    )

    class Meta:
        model = BranchSettings
        fields = [
            'branch', 'branch_id', 'trainers', 'trainers_id', 'is_unisex', 'type', 'phone_number', 'is_active', 'created_at', 'created_by', 'updated_at'
        ]


class CombinedBranchWithSettingsSerializer(serializers.Serializer):
    """Serializer for the combned branch and branch settings api."""

    branch = BranchSerializer()
    branch_settings = BranchSettingsSerializer()

    def create(self, validated_data):

        branch = validated_data.pop('branch', None)
        branch_settings = validated_data.pop('branch_settings', None)

        user = self.context.get('user')

        branch['created_by'] = user

        with transaction.atomic():

            obj = Branch.objects.create(**branch)

            for bs in branch_settings:
                BranchSettings.objects.create(
                    branch=obj,
                    **bs
                )

            b_data = BranchSerializer(obj).data
            bs_data = BranchSettingsSerializer(b_data, many=True)

        return {
            'branch': b_data,
            'branch_settings': bs_data,
        }
