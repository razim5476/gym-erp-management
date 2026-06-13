"""
Docstring for core.views
"""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
from core.permissions import constants
from core.permissions.base_permission import GuardianPermission
from .serializers.serializers import (
    BarcodesSerializer,
    BrandSerializer,
    CategorySerializer,
    CountrySerializer,
    CurrencySerializer,
    FinancialYearSerializer,
    PaginationSizeSerializer,
    StateSerializer,
    SubCategorySerializer,
    UniqueIdSerializer,
    UnitOfMeasureSerializer,
)


class StandardPageNumberPagination(PageNumberPagination):
    """
    For using pagination size from frontend like 20, 30, 50, etc.
    """

    page_size = 50  # default
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        requested_size = request.query_params.get(self.page_size_query_param)

        allowed_sizes = PaginationSize.objects.filter(
            is_active=True
        ).values_list('data_per_page', flat=True)

        if requested_size and requested_size.isdigit():
            requested_size = int(requested_size)

            if requested_size in allowed_sizes:
                return requested_size

        return self.page_size


class CoreModelViewSet(viewsets.ModelViewSet):
    """
    Common core CRUD behaviour with Guardian object permissions.
    """

    pagination_class = StandardPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, GuardianPermission]
    company_branch_scoped = False
    branch_relation_scoped = False

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()

        queryset = get_objects_for_user(
            user,
            self.permission_map["list"],
            klass=self.queryset.model
        )

        if self.company_branch_scoped:
            queryset = queryset.filter(company=user.company, branch=user.branch)

        if self.branch_relation_scoped:
            queryset = queryset.filter(branch_id=user.branch)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        save_kwargs = {
            "created_by": user.id
        }

        if self.company_branch_scoped:
            save_kwargs.update({
                "company": user.company,
                "branch": user.branch
            })

        obj = serializer.save(**save_kwargs)

        assign_perm(self.permission_map["list"], user, obj)
        assign_perm(self.permission_map["update"], user, obj)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def soft_delete_object(self, pk, model, permission, object_name):
        user = self.request.user
        obj = get_object_or_404(model, pk=pk)

        if not user.has_perm(permission, obj):
            raise PermissionDenied(
                f"You don't have permission to disable this {object_name}"
            )

        obj.is_active = False
        obj.save()

        return Response({
            "message": f"{object_name.title()} disabled successfully."
        }, status=status.HTTP_200_OK)


class CountryViewSet(CoreModelViewSet):
    """
    Country CRUD APIs.
    """

    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    permission_map = {
        "list": constants.CountryPermissions.VIEW_COUNTRY,
        "retrieve": constants.CountryPermissions.VIEW_COUNTRY,
        "create": constants.CountryPermissions.CREATE_COUNTRY,
        "update": constants.CountryPermissions.EDIT_COUNTRY,
        "partial_update": constants.CountryPermissions.EDIT_COUNTRY,
        "destroy": constants.CountryPermissions.DELETE_COUNTRY,
        "country_soft_delete": constants.CountryPermissions.DISABLE_COUNTRY
    }

    @action(
        url_name='country_soft_delete',
        methods=['POST'],
        url_path='country_soft_delete',
        detail=True
    )
    def country_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, Country, constants.CountryPermissions.DISABLE_COUNTRY, "country"
        )


class StateViewSet(CoreModelViewSet):
    """
    State CRUD APIs.
    """

    serializer_class = StateSerializer
    queryset = State.objects.all()

    permission_map = {
        "list": constants.StatePermissions.VIEW_STATE,
        "retrieve": constants.StatePermissions.VIEW_STATE,
        "create": constants.StatePermissions.CREATE_STATE,
        "update": constants.StatePermissions.EDIT_STATE,
        "partial_update": constants.StatePermissions.EDIT_STATE,
        "destroy": constants.StatePermissions.DELETE_STATE,
        "state_soft_delete": constants.StatePermissions.DISABLE_STATE
    }

    @action(
        url_name='state_soft_delete',
        methods=['POST'],
        url_path='state_soft_delete',
        detail=True
    )
    def state_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, State, constants.StatePermissions.DISABLE_STATE, "state"
        )


class CurrencyViewSet(CoreModelViewSet):
    """
    Currency CRUD APIs.
    """

    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

    permission_map = {
        "list": constants.CurrencyPermissions.VIEW_CURRENCY,
        "retrieve": constants.CurrencyPermissions.VIEW_CURRENCY,
        "create": constants.CurrencyPermissions.CREATE_CURRENCY,
        "update": constants.CurrencyPermissions.EDIT_CURRENCY,
        "partial_update": constants.CurrencyPermissions.EDIT_CURRENCY,
        "destroy": constants.CurrencyPermissions.DELETE_CURRENCY,
        "currency_soft_delete": constants.CurrencyPermissions.DISABLE_CURRENCY
    }

    @action(
        url_name='currency_soft_delete',
        methods=['POST'],
        url_path='currency_soft_delete',
        detail=True
    )
    def currency_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, Currency, constants.CurrencyPermissions.DISABLE_CURRENCY,
            "currency"
        )


class UnitOfMeasureViewSet(CoreModelViewSet):
    """
    Unit Of Measure CRUD APIs.
    """

    serializer_class = UnitOfMeasureSerializer
    queryset = UnitOfMeasure.objects.all()

    permission_map = {
        "list": constants.UnitOfMeasurePermissions.VIEW_UOM,
        "retrieve": constants.UnitOfMeasurePermissions.VIEW_UOM,
        "create": constants.UnitOfMeasurePermissions.CREATE_UOM,
        "update": constants.UnitOfMeasurePermissions.EDIT_UOM,
        "partial_update": constants.UnitOfMeasurePermissions.EDIT_UOM,
        "destroy": constants.UnitOfMeasurePermissions.DELETE_UOM,
        "uom_soft_delete": constants.UnitOfMeasurePermissions.DISABLE_UOM
    }

    @action(
        url_name='uom_soft_delete',
        methods=['POST'],
        url_path='uom_soft_delete',
        detail=True
    )
    def uom_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, UnitOfMeasure, constants.UnitOfMeasurePermissions.DISABLE_UOM,
            "unit of measure"
        )


class BrandViewSet(CoreModelViewSet):
    """
    Brand CRUD APIs.
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    company_branch_scoped = True

    permission_map = {
        "list": constants.BrandPermissions.VIEW_BRAND,
        "retrieve": constants.BrandPermissions.VIEW_BRAND,
        "create": constants.BrandPermissions.CREATE_BRAND,
        "update": constants.BrandPermissions.EDIT_BRAND,
        "partial_update": constants.BrandPermissions.EDIT_BRAND,
        "destroy": constants.BrandPermissions.DELETE_BRAND,
        "brand_soft_delete": constants.BrandPermissions.DISABLE_BRAND
    }

    @action(
        url_name='brand_soft_delete',
        methods=['POST'],
        url_path='brand_soft_delete',
        detail=True
    )
    def brand_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, Brand, constants.BrandPermissions.DISABLE_BRAND, "brand"
        )


class CategoryViewSet(CoreModelViewSet):
    """
    Category CRUD APIs.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    company_branch_scoped = True

    permission_map = {
        "list": constants.CategoryPermissions.VIEW_CATEGORY,
        "retrieve": constants.CategoryPermissions.VIEW_CATEGORY,
        "create": constants.CategoryPermissions.CREATE_CATEGORY,
        "update": constants.CategoryPermissions.EDIT_CATEGORY,
        "partial_update": constants.CategoryPermissions.EDIT_CATEGORY,
        "destroy": constants.CategoryPermissions.DELETE_CATEGORY,
        "category_soft_delete": constants.CategoryPermissions.DISABLE_CATEGORY
    }

    @action(
        url_name='category_soft_delete',
        methods=['POST'],
        url_path='category_soft_delete',
        detail=True
    )
    def category_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, Category, constants.CategoryPermissions.DISABLE_CATEGORY,
            "category"
        )


class SubCategoryViewSet(CoreModelViewSet):
    """
    Sub Category CRUD APIs.
    """

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    company_branch_scoped = True

    permission_map = {
        "list": constants.SubCategoryPermissions.VIEW_SUB_CATEGORY,
        "retrieve": constants.SubCategoryPermissions.VIEW_SUB_CATEGORY,
        "create": constants.SubCategoryPermissions.CREATE_SUB_CATEGORY,
        "update": constants.SubCategoryPermissions.EDIT_SUB_CATEGORY,
        "partial_update": constants.SubCategoryPermissions.EDIT_SUB_CATEGORY,
        "destroy": constants.SubCategoryPermissions.DELETE_SUB_CATEGORY,
        "sub_category_soft_delete": (
            constants.SubCategoryPermissions.DISABLE_SUB_CATEGORY
        )
    }

    @action(
        url_name='sub_category_soft_delete',
        methods=['POST'],
        url_path='sub_category_soft_delete',
        detail=True
    )
    def sub_category_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, SubCategory,
            constants.SubCategoryPermissions.DISABLE_SUB_CATEGORY,
            "sub category"
        )


class BarcodesViewSet(CoreModelViewSet):
    """
    Barcode CRUD APIs.
    """

    serializer_class = BarcodesSerializer
    queryset = Barcodes.objects.all()

    permission_map = {
        "list": constants.BarcodePermissions.VIEW_BARCODE,
        "retrieve": constants.BarcodePermissions.VIEW_BARCODE,
        "create": constants.BarcodePermissions.CREATE_BARCODE,
        "update": constants.BarcodePermissions.EDIT_BARCODE,
        "partial_update": constants.BarcodePermissions.EDIT_BARCODE,
        "destroy": constants.BarcodePermissions.DELETE_BARCODE,
        "barcode_soft_delete": constants.BarcodePermissions.DISABLE_BARCODE
    }

    @action(
        url_name='barcode_soft_delete',
        methods=['POST'],
        url_path='barcode_soft_delete',
        detail=True
    )
    def barcode_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, Barcodes, constants.BarcodePermissions.DISABLE_BARCODE,
            "barcode"
        )


class PaginationSizeViewSet(CoreModelViewSet):
    """
    Pagination Size CRUD APIs.
    """

    serializer_class = PaginationSizeSerializer
    queryset = PaginationSize.objects.all()

    permission_map = {
        "list": constants.PaginationSizePermissions.VIEW_PAGINATION_SIZE,
        "retrieve": constants.PaginationSizePermissions.VIEW_PAGINATION_SIZE,
        "create": constants.PaginationSizePermissions.CREATE_PAGINATION_SIZE,
        "update": constants.PaginationSizePermissions.EDIT_PAGINATION_SIZE,
        "partial_update": (
            constants.PaginationSizePermissions.EDIT_PAGINATION_SIZE
        ),
        "destroy": constants.PaginationSizePermissions.DELETE_PAGINATION_SIZE,
        "pagination_size_soft_delete": (
            constants.PaginationSizePermissions.DISABLE_PAGINATION_SIZE
        )
    }

    @action(
        url_name='pagination_size_soft_delete',
        methods=['POST'],
        url_path='pagination_size_soft_delete',
        detail=True
    )
    def pagination_size_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, PaginationSize,
            constants.PaginationSizePermissions.DISABLE_PAGINATION_SIZE,
            "pagination size"
        )


class UniqueIdViewSet(CoreModelViewSet):
    """
    Unique Id CRUD APIs.
    """

    serializer_class = UniqueIdSerializer
    queryset = UniqueId.objects.all()
    branch_relation_scoped = True

    permission_map = {
        "list": constants.UniqueIdPermissions.VIEW_UNIQUE_ID,
        "retrieve": constants.UniqueIdPermissions.VIEW_UNIQUE_ID,
        "create": constants.UniqueIdPermissions.CREATE_UNIQUE_ID,
        "update": constants.UniqueIdPermissions.EDIT_UNIQUE_ID,
        "partial_update": constants.UniqueIdPermissions.EDIT_UNIQUE_ID,
        "destroy": constants.UniqueIdPermissions.DELETE_UNIQUE_ID,
        "unique_id_soft_delete": constants.UniqueIdPermissions.DISABLE_UNIQUE_ID
    }

    @action(
        url_name='unique_id_soft_delete',
        methods=['POST'],
        url_path='unique_id_soft_delete',
        detail=True
    )
    def unique_id_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, UniqueId, constants.UniqueIdPermissions.DISABLE_UNIQUE_ID,
            "unique id"
        )


class FinancialYearViewSet(CoreModelViewSet):
    """
    Financial Year CRUD APIs.
    """

    serializer_class = FinancialYearSerializer
    queryset = FinancialYear.objects.all()

    permission_map = {
        "list": constants.FinancialYearPermissions.VIEW_FINANCIAL_YEAR,
        "retrieve": constants.FinancialYearPermissions.VIEW_FINANCIAL_YEAR,
        "create": constants.FinancialYearPermissions.CREATE_FINANCIAL_YEAR,
        "update": constants.FinancialYearPermissions.EDIT_FINANCIAL_YEAR,
        "partial_update": (
            constants.FinancialYearPermissions.EDIT_FINANCIAL_YEAR
        ),
        "destroy": constants.FinancialYearPermissions.DELETE_FINANCIAL_YEAR,
        "financial_year_soft_delete": (
            constants.FinancialYearPermissions.DISABLE_FINANCIAL_YEAR
        )
    }

    @action(
        url_name='financial_year_soft_delete',
        methods=['POST'],
        url_path='financial_year_soft_delete',
        detail=True
    )
    def financial_year_soft_delete(self, request, pk=None):
        return self.soft_delete_object(
            pk, FinancialYear,
            constants.FinancialYearPermissions.DISABLE_FINANCIAL_YEAR,
            "financial year"
        )


