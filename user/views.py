"""
User views.
"""


from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.views import StandardPageNumberPagination
from user.models import User
from user.serializers.serializers import UserSerialzier


class MembershipViewSet(ModelViewSet):
    """
    CRUD APIs for member users.
    """

    serializer_class = UserSerialzier
    pagination_class = StandardPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['created_at', 'joined_date', 'first_name', 'last_name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = User.objects.filter(userr_type='Member')
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(company=user.company, branch=user.branch)

    def perform_create(self, serializer):
        serializer.save(
            userr_type='Member',
            company=self.request.user.company,
            branch=self.request.user.branch
        )

    def perform_update(self, serializer):
        serializer.save(userr_type='Member')
