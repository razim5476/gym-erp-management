"""
User views.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.responses import error_response, success_response
from core.views import StandardPageNumberPagination
from user.models import (
    Address,
    Attendance,
    Gallery,
    LoginLog,
    Permission,
    Role,
    Trainer,
    User,
    UserProfile,
)
from user.serializers.serializers import (
    AddressSerializer,
    AttendanceSerializer,
    GallerySerializer,
    LoginLogSerializer,
    MemberSerialzier,
    PermissionSerializer,
    RoleSerializer,
    TrainerSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from user.services.services import UserServices


class UserBaseAPIView(APIView):
    """
    Reusable CRUD behaviour for user app models using APIView.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = None
    queryset = None
    search_fields = []
    ordering_fields = ["created_at", "updated_at"]
    default_ordering = "-created_at"
    filter_fields = ["is_active"]
    object_name = "record"

    def get_base_queryset(self):
        return self.queryset.all()

    def get_queryset(self):
        return self.get_base_queryset()

    def get_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", {"request": self.request})
        return self.serializer_class(*args, **kwargs)

    def filter_queryset(self, queryset):
        query = self.request.query_params.get("search")
        if query and self.search_fields:
            search_q = Q()
            for field in self.search_fields:
                search_q |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(search_q)

        for field in self.filter_fields:
            value = self.request.query_params.get(field)
            if value in [None, ""]:
                continue
            lookup = field if "__" in field else f"{field}__exact"
            queryset = queryset.filter(**{lookup: value})

        ordering = self.request.query_params.get("ordering")
        if ordering:
            clean_ordering = ordering.lstrip("-")
            if clean_ordering in self.ordering_fields:
                queryset = queryset.order_by(ordering)
        elif self.default_ordering:
            queryset = queryset.order_by(self.default_ordering)

        return queryset

    def paginate_queryset(self, queryset):
        paginator = StandardPageNumberPagination()
        page = paginator.paginate_queryset(queryset, self.request, view=self)
        return paginator, page

    def paginated_payload(self, paginator, page, serializer):
        return {
            "results": serializer.data,
            "pagination": {
                "count": paginator.page.paginator.count,
                "page": paginator.page.number,
                "page_size": paginator.get_page_size(self.request),
                "total_pages": paginator.page.paginator.num_pages,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
            },
        }

    def get(self, request, pk=None):
        if pk is not None:
            obj = self.get_object(pk)
            serializer = self.get_serializer(obj)
            return success_response(
                message=f"{self.object_name.title()} fetched successfully.",
                data=serializer.data,
            )

        queryset = self.filter_queryset(self.get_queryset())
        paginator, page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return success_response(
            message=f"{self.object_name.title()} list fetched successfully.",
            data=self.paginated_payload(paginator, page, serializer),
        )

    def get_save_kwargs(self):
        return {}

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        obj = serializer.save(**self.get_save_kwargs())
        return success_response(
            message=f"{self.object_name.title()} created successfully.",
            data=self.get_serializer(obj).data,
            status_code=status.HTTP_201_CREATED,
        )

    def put(self, request, pk):
        return self.update(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def update(self, request, pk, partial=False):
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        obj = serializer.save(**self.get_save_kwargs())
        return success_response(
            message=f"{self.object_name.title()} updated successfully.",
            data=self.get_serializer(obj).data,
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if hasattr(obj, "is_active"):
            obj.is_active = False
            obj.save(update_fields=["is_active"])
        else:
            obj.delete()

        return success_response(
            message=f"{self.object_name.title()} deleted successfully."
        )


class UserAPIView(UserBaseAPIView):
    """
    User CRUD APIs.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    object_name = "user"
    search_fields = [
        "user_id", "first_name", "last_name", "username", "email",
        "phone_number",
    ]
    ordering_fields = [
        "created_at", "updated_at", "joined_date", "first_name",
        "last_name", "username", "email",
    ]
    filter_fields = ["is_active", "company", "branch", "is_staff"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(company=user.company, branch=user.branch)

    def get_save_kwargs(self):
        user = self.request.user
        if user.is_superuser:
            return {}
        return {
            "company": user.company,
            "branch": user.branch,
        }


class MembershipAPIView(UserAPIView):
    """
    Member CRUD APIs with generated login credentials.
    """

    serializer_class = MemberSerialzier
    object_name = "member"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        credentials = UserServices.MemberServices.create_member_login_credentials(
            request=request,
            firstname=serializer.validated_data.get("first_name", ""),
            lastname=serializer.validated_data.get("last_name", ""),
        )
        user = serializer.save(username=credentials["username"])
        user.set_password(credentials["temp_password"])
        user.save(update_fields=["password"])

        data = self.get_serializer(user).data
        data["credentials"] = credentials

        return success_response(
            message="Member created successfully.",
            data=data,
            status_code=status.HTTP_201_CREATED,
        )


class LoginLogAPIView(UserBaseAPIView):
    """
    Login log CRUD APIs.
    """

    serializer_class = LoginLogSerializer
    queryset = LoginLog.objects.select_related("user")
    object_name = "login log"
    search_fields = ["login_log_id", "description", "user__username"]
    ordering_fields = ["created_at", "updated_at"]
    filter_fields = ["is_active", "user"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user__company=user.company, user__branch=user.branch)


class AddressAPIView(UserBaseAPIView):
    """
    Address CRUD APIs.
    """

    serializer_class = AddressSerializer
    queryset = Address.objects.select_related("user", "country", "state")
    object_name = "address"
    search_fields = [
        "address_id", "name", "address_line_1", "city", "pincode",
        "user__username", "user__email",
    ]
    ordering_fields = ["created_at", "updated_at", "name", "city"]
    filter_fields = ["is_active", "user", "country", "state", "address_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user__company=user.company, user__branch=user.branch)


class AttendanceAPIView(UserBaseAPIView):
    """
    Attendance CRUD APIs.
    """

    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.select_related("user")
    object_name = "attendance"
    search_fields = [
        "attendance_id", "attendence_for", "status", "user__username",
        "user__email",
    ]
    ordering_fields = ["created_at", "updated_at", "start_time", "end_time"]
    filter_fields = ["is_active", "user", "status", "attendence_for"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user__company=user.company, user__branch=user.branch)


class RoleAPIView(UserBaseAPIView):
    """
    Role CRUD APIs.
    """

    serializer_class = RoleSerializer
    queryset = Role.objects.prefetch_related("permission")
    object_name = "role"
    search_fields = ["role_id", "name", "descritpiton"]
    ordering_fields = ["created_at", "updated_at", "name"]
    filter_fields = ["is_active"]


class PermissionAPIView(UserBaseAPIView):
    """
    Permission CRUD APIs.
    """

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    object_name = "permission"
    search_fields = ["permission_id", "name", "code", "description"]
    ordering_fields = ["created_at", "updated_at", "name", "code"]
    filter_fields = ["is_active"]


class UserProfileAPIView(UserBaseAPIView):
    """
    User profile CRUD APIs.
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.select_related("user")
    object_name = "user profile"
    search_fields = ["user__username", "user__email", "bio", "blood_group"]
    ordering_fields = ["created_at", "updated_at", "level"]
    filter_fields = ["is_active", "user", "level", "blood_group"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user__company=user.company, user__branch=user.branch)


class GalleryAPIView(UserBaseAPIView):
    """
    Gallery CRUD APIs.
    """

    serializer_class = GallerySerializer
    queryset = Gallery.objects.select_related("user", "user__user")
    object_name = "gallery"
    search_fields = ["user__user__username", "user__user__email"]
    ordering_fields = ["created_at", "updated_at"]
    filter_fields = ["is_active", "user"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(
            user__user__company=user.company,
            user__user__branch=user.branch,
        )


class TrainerAPIView(UserBaseAPIView):
    """
    Trainer CRUD APIs.
    """

    serializer_class = TrainerSerializer
    queryset = Trainer.objects.select_related("user", "category")
    object_name = "trainer"
    search_fields = [
        "user__username", "user__email", "experience", "bio",
    ]
    ordering_fields = [
        "created_at", "updated_at", "joined_date", "salary", "level",
    ]
    filter_fields = ["is_active", "user", "category", "level", "on_leave"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user__company=user.company, user__branch=user.branch)
