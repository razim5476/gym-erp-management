"""
Docstring for accounts.views
"""


from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, assign_perm
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.models import AccountGroups, Accounts
from core.permissions.base_permission import GuardianPermission
from core.views import StandardPageNumberPagination
from .serializers import serializers
from core.permissions import constants
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class AccountGroupViewSet(ModelViewSet):
    """
    Docstring for AccountGroupViewSet
    """

    serializer_class = serializers.AccountGroupSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]
    queryset = AccountGroups.objects.all()

    permission_map = {
        "list": constants.AccountGroupPermissions.VIEW_GROUP,
        "retrieve": constants.AccountGroupPermissions.VIEW_GROUP,
        "create": constants.AccountGroupPermissions.CREATE_GROUP,
        "update": constants.AccountGroupPermissions.EDIT_GROUP,
        "partial_update": constants.AccountGroupPermissions.EDIT_GROUP,
        "destroy": constants.AccountGroupPermissions.DELETE_GROUP,
        "soft_delete": constants.AccountGroupPermissions.DISABLE_GROUP
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return AccountGroups.objects.all()
        
        return get_objects_for_user(
            user,
            constants.AccountGroupPermissions.VIEW_GROUP,
            klass=AccountGroups
        ).filter(
            company=user.company,
            branch=user.branch
        )
    
    def perform_create(self, serializer):
        user = self.request.user

        obj = serializer.save(
            company=user.company,
            branch=user.branch,
            created_by=user
        )

        assign_perm(constants.AccountGroupPermissions.VIEW_GROUP, user, obj)
        assign_perm(constants.AccountGroupPermissions.EDIT_GROUP, user, obj)

    def perform_update(self, serializer):
        user = self.request.user

        obj = serializer.save(
            updated_by=user
        )

    @action(
        url_name='account_group_soft_delete',
        methods=['POST'], 
        url_path='account_group_soft_delete',
        detail=True
    )
    def account_group_soft_delete(self, request, id):

        user = self.request.user

        obj = get_object_or_404(AccountGroups, pk=id)

        if not user.has_perm(
            constants.AccountGroupPermissions.DISABLE_GROUP, obj
        ):
            raise PermissionDenied("You don't have permission to disable this account group")
        
        obj.is_active = True
        obj.save()
        
        return Response({
            "message": "Account Group disabled successfully."
        }, status=status.HTTP_200_OK)



class AccountViewSet(ModelViewSet):
    """
    Docstring for AccountViewSet
    """

    serializer_class = serializers.AccountSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated, GuardianPermission]
    queryset = Accounts.objects.all()

    permission_map = {
        "list": constants.AccountPermissions.VIEW_ACCOUNT,
        "retrieve": constants.AccountPermissions.VIEW_ACCOUNT,
        "create": constants.AccountPermissions.CREATE_ACCOUNT,
        "update": constants.AccountPermissions.EDIT_ACCOUNT,
        "partial_update": constants.AccountPermissions.EDIT_ACCOUNT,
        "destroy": constants.AccountPermissions.DELETE_ACCOUNT,
        "soft_delete": constants.AccountPermissions.DISABLE_ACCOUNT
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Accounts.objects.all()
        
        return get_objects_for_user(
            user,
            constants.AccountPermissions.VIEW_ACCOUNT,
            klass=Accounts
        ).filter(
            company=user.company,
            branch=user.branch
        )
    
    def perform_create(self, serializer):
        user = self.request.user

        obj = serializer.save(
            company=user.company,
            branch=user.branch,
            created_by=user
        )

        assign_perm(constants.AccountPermissions.VIEW_ACCOUNT, user, obj)
        assign_perm(constants.AccountPermissions.EDIT_ACCOUNT, user, obj)

    def perform_update(self, serializer):
        user = self.request.user

        obj = serializer.save(
            updated_by=user
        )
    
    @action(
        url_name='account_soft_delete',
        methods=['POST'],
        url_path='account_soft_delete',
        detail=True
    )
    def account_soft_delete(self, request, id):
        user = self.request.user

        obj = get_object_or_404(Accounts, pk=id)

        if not user.has_perm(
            constants.AccountPermissions.DISABLE_ACCOUNT
        ):
            raise PermissionDenied(
                "You don't have permission to disable this account group"
            )
        
        obj.is_active = False
        obj.save()

        return Response({
            "message": "Account disable successfully."
        }, status=status.HTTP_200_OK)
    


class BankViewSet(ModelViewSet):
    """
    BankViewSet
    """