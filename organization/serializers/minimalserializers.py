"""
Docstring for organization.serializers.minimalserializers
"""

from rest_framework import serializers

from organization.models import Branch, Company



class MinimalCompanySerializer(serializers.ModelSerializer):
    """
    MinimmalCompanySerializer
    """

    class Meta:
        model = Company
        fields = [
            'company_id', 'name'
        ]


class MinimalBranchSerializer(serializers.ModelSerializer):
    """
    MinimialBranchSerializer
    """

    class Meta:
        model = Branch
        fields = [
            'branch_id', 'name'
        ]

