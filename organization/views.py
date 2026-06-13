"""
Organization views
"""

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from core.permissions import constants
from core.utils import generate_unique_id
from core.views import StandardPageNumberPagination
from organization.models import Company
from organization.serializers.serializers import CombinedCompanyCreateSerializer, CompanySerializer
from guardian.shortcuts import get_objects_for_user, assign_perm
# Create your views here.


class CompanyCreateViewSet(generics.CreateAPIView):
    """
    Company related APIs
    """

    serializer_class = CombinedCompanyCreateSerializer
    pagination_class = StandardPageNumberPagination
    queryset = Company.objects.all()


    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Company.objects.all()
        
        return get_objects_for_user(
            user,
            constants.CompanyPermissions.VIEW_COMPANY,
            klass=Company
        ).filter(
            company=user.company,
            branch=user.branch
        )
    
    def perform_create(self, serializer):
        user = self.request.user

        obj = serializer.save()

        assign_perm(constants.CompanyPermissions.VIEW_COMPANY, user, obj["company"])
        assign_perm(constants.CompanyPermissions.EDIT_COMPANY, user, obj["company"])


class CompanySoftDeleteAPIView(generics.UpdateAPIView):
    """
    Company Soft delete.
    """

    def post(self, request, id):

        user = self.request.user

        obj = get_object_or_404(Company, pk=id)

        if not user.has_perm(
            constants.CompanyPermissions.DISABLE_COMPANY, obj["company"]
        ):
            raise PermissionDenied("You don't have permission to disable this company")
        
        obj.is_active = False
        obj.save()
        
        return Response({
            "message": "Company disabled successfully."
        }, status=status.HTTP_200_OK)



