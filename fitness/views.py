"""
Fitness views.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from core.views import StandardPageNumberPagination
from fitness.models import (
    Diet,
    DietDetail,
    Item,
    ItemCategory,
    ItemMacros,
    MembershipPlan,
    Playlist,
    PlaylistSongs,
    TrainerCategory,
    Workouts,
    WorkoutsPlan,
)
from fitness.serializers.minimalserializers import (
    MinimalDietSerializer,
    MinimalItemCategorySerializer,
    MinimalItemSerializer,
    MinimalMembershipPlanSerializer,
    MinimalPlaylistSerializer,
    MinimalTrainerCategorySerializer,
    MinimalWorkoutPlanSerializer,
    MinimalWorkoutSerializer,
)
from fitness.serializers.serializers import (
    DietDetailSerializer,
    DietSerializer,
    ItemCategorySerializer,
    ItemMacrosSerializer,
    ItemSerializer,
    MembershipPlanSerializers,
    PlaylistSerializer,
    PlaylistSongSerializer,
    TrainerCategorySerializer,
    WorkoutPlanSerializer,
    WorkoutSerializer,
)


class FitnessModelViewSet(viewsets.ModelViewSet):
    """
    Common CRUD behaviour for fitness models.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = StandardPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    tenant_scoped = False
    parent_scope = None
    filterset_fields = ['is_active']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = self.queryset.all()
        user = self.request.user

        if user.is_superuser:
            return queryset

        if self.tenant_scoped:
            return queryset.filter(company=user.company, branch=user.branch)

        if self.parent_scope:
            return queryset.filter(
                **{
                    f'{self.parent_scope}__company': user.company,
                    f'{self.parent_scope}__branch': user.branch,
                }
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        save_kwargs = {'created_by': user}

        if self.tenant_scoped:
            save_kwargs.update({
                'company': user.company,
                'branch': user.branch,
            })

        serializer.save(**save_kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        if hasattr(instance, 'is_active'):
            instance.is_active = False
            instance.save(update_fields=['is_active'])
            return

        instance.delete()


class FitnessDropdownViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Base read-only dropdown viewset for fitness models.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = StandardPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    tenant_scoped = False
    parent_scope = None
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = self.queryset.filter(is_active=True)
        user = self.request.user

        if user.is_superuser:
            return queryset

        if self.tenant_scoped:
            return queryset.filter(company=user.company, branch=user.branch)

        if self.parent_scope:
            return queryset.filter(
                **{
                    f'{self.parent_scope}__company': user.company,
                    f'{self.parent_scope}__branch': user.branch,
                }
            )

        return queryset


class TrainerCategoryViewSet(FitnessModelViewSet):
    """
    Trainer category CRUD APIs.
    """

    serializer_class = TrainerCategorySerializer
    queryset = TrainerCategory.objects.all()
    search_fields = ['trainer_category_id', 'name']
    ordering_fields = ['name', 'created_at', 'updated_at']


class TrainerCategoryDropdownViewSet(FitnessDropdownViewSet):
    """
    Trainer category dropdown APIs.
    """

    serializer_class = MinimalTrainerCategorySerializer
    queryset = TrainerCategory.objects.all()
    search_fields = ['trainer_category_id', 'name']


class WorkoutViewSet(FitnessModelViewSet):
    """
    Workout CRUD APIs.
    """

    serializer_class = WorkoutSerializer
    queryset = Workouts.objects.all()
    tenant_scoped = True
    search_fields = ['workout_id', 'name', 'body_part']
    filterset_fields = ['is_active', 'body_part']
    ordering_fields = ['name', 'body_part', 'created_at', 'updated_at']


class WorkoutDropdownViewSet(FitnessDropdownViewSet):
    """
    Workout dropdown APIs.
    """

    serializer_class = MinimalWorkoutSerializer
    queryset = Workouts.objects.all()
    tenant_scoped = True
    search_fields = ['workout_id', 'name', 'body_part']
    filterset_fields = ['is_active', 'body_part']


class WorkoutPlanViewSet(FitnessModelViewSet):
    """
    Workout plan CRUD APIs.
    """

    serializer_class = WorkoutPlanSerializer
    queryset = WorkoutsPlan.objects.prefetch_related('excersises')
    tenant_scoped = True
    search_fields = ['workout_id', 'name', 'gender', 'difficulty']
    filterset_fields = ['is_active', 'gender', 'difficulty']
    ordering_fields = ['name', 'created_at', 'updated_at']


class WorkoutPlanDropdownViewSet(FitnessDropdownViewSet):
    """
    Workout plan dropdown APIs.
    """

    serializer_class = MinimalWorkoutPlanSerializer
    queryset = WorkoutsPlan.objects.all()
    tenant_scoped = True
    search_fields = ['workout_id', 'name']
    filterset_fields = ['is_active', 'gender', 'difficulty']


class PlaylistViewSet(FitnessModelViewSet):
    """
    Playlist CRUD APIs.
    """

    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()
    tenant_scoped = True
    search_fields = ['playlist_id', 'name', 'platform']
    filterset_fields = ['is_active', 'platform']
    ordering_fields = ['name', 'created_at', 'updated_at']


class PlaylistDropdownViewSet(FitnessDropdownViewSet):
    """
    Playlist dropdown APIs.
    """

    serializer_class = MinimalPlaylistSerializer
    queryset = Playlist.objects.all()
    tenant_scoped = True
    search_fields = ['playlist_id', 'name', 'platform']


class PlaylistSongViewSet(FitnessModelViewSet):
    """
    Playlist song CRUD APIs.
    """

    serializer_class = PlaylistSongSerializer
    queryset = PlaylistSongs.objects.select_related('playlist')
    parent_scope = 'playlist'
    search_fields = ['title', 'playlist_url', 'playlist__name']
    filterset_fields = ['is_active', 'playlist']
    ordering_fields = ['title', 'created_at', 'updated_at']


class DietViewSet(FitnessModelViewSet):
    """
    Diet CRUD APIs.
    """

    serializer_class = DietSerializer
    queryset = Diet.objects.all()
    tenant_scoped = True
    search_fields = ['diet_id', 'name', 'diet_type', 'goal_type']
    filterset_fields = ['is_active', 'diet_type', 'goal_type']
    ordering_fields = ['name', 'created_at', 'updated_at']


class DietDropdownViewSet(FitnessDropdownViewSet):
    """
    Diet dropdown APIs.
    """

    serializer_class = MinimalDietSerializer
    queryset = Diet.objects.all()
    tenant_scoped = True
    search_fields = ['diet_id', 'name']
    filterset_fields = ['is_active', 'diet_type', 'goal_type']


class DietDetailViewSet(FitnessModelViewSet):
    """
    Diet detail CRUD APIs.
    """

    serializer_class = DietDetailSerializer
    queryset = DietDetail.objects.select_related('diet').prefetch_related('food_items')
    parent_scope = 'diet'
    search_fields = ['diet_day', 'part_of_day', 'diet__name']
    filterset_fields = ['is_active', 'diet', 'diet_day', 'part_of_day']
    ordering_fields = ['diet_day', 'created_at', 'updated_at']


class ItemCategoryViewSet(FitnessModelViewSet):
    """
    Food item category CRUD APIs.
    """

    serializer_class = ItemCategorySerializer
    queryset = ItemCategory.objects.all()
    search_fields = ['item_category_id', 'name']
    ordering_fields = ['name', 'created_at', 'updated_at']


class ItemCategoryDropdownViewSet(FitnessDropdownViewSet):
    """
    Food item category dropdown APIs.
    """

    serializer_class = MinimalItemCategorySerializer
    queryset = ItemCategory.objects.all()
    search_fields = ['item_category_id', 'name']


class ItemViewSet(FitnessModelViewSet):
    """
    Food item CRUD APIs.
    """

    serializer_class = ItemSerializer
    queryset = Item.objects.select_related('category', 'uom')
    search_fields = ['item_id', 'name', 'category__name']
    filterset_fields = ['is_active', 'category', 'uom']
    ordering_fields = ['name', 'created_at', 'updated_at']


class ItemDropdownViewSet(FitnessDropdownViewSet):
    """
    Food item dropdown APIs.
    """

    serializer_class = MinimalItemSerializer
    queryset = Item.objects.all()
    search_fields = ['item_id', 'name']
    filterset_fields = ['is_active', 'category']


class ItemMacrosViewSet(FitnessModelViewSet):
    """
    Food item macros CRUD APIs.
    """

    serializer_class = ItemMacrosSerializer
    queryset = ItemMacros.objects.select_related('item')
    search_fields = ['item_macros_id', 'item__name']
    filterset_fields = ['is_active', 'item']
    ordering_fields = ['created_at', 'updated_at', 'calories', 'protein']


class MembershipPlanViewSet(FitnessModelViewSet):
    """
    Membership plan CRUD APIs.
    """

    serializer_class = MembershipPlanSerializers
    queryset = MembershipPlan.objects.all()
    tenant_scoped = True
    search_fields = ['membershipl_plan_id', 'name', 'plan_period']
    filterset_fields = ['is_active', 'plan_period', 'allow_freeze']
    ordering_fields = ['name', 'price', 'created_at', 'updated_at']


class MembershipPlanDropdown(FitnessDropdownViewSet):
    """
    Membership plan dropdown APIs.
    """

    serializer_class = MinimalMembershipPlanSerializer
    queryset = MembershipPlan.objects.all()
    tenant_scoped = True
    search_fields = ['membershipl_plan_id', 'name', 'plan_period']
    filterset_fields = ['is_active', 'plan_period', 'allow_freeze']
