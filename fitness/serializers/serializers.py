"""
Fitness serializers.
"""

import uuid

from rest_framework import serializers

from accounts.models import TaxGroups
from core.models import UnitOfMeasure
from core.serializers.minimal_serializers import MinimalUnitOfMeasureSerializer
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
    MinimalPlaylistSerializer,
    MinimalWorkoutSerializer,
)
from organization.serializers.minimalserializers import (
    MinimalBranchSerializer,
    MinimalCompanySerializer,
)
from user.serializers.minimalserializers import MinimalUserSerializer


def make_fitness_id(prefix):
    """
    Generate compact readable IDs when the client does not send one.
    """

    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


class FitnessAuditMixin(serializers.ModelSerializer):
    """
    Shared read-only audit fields for fitness serializers.
    """

    created_by = MinimalUserSerializer(read_only=True)
    updated_by = MinimalUserSerializer(read_only=True)


class TenantScopedSerializer(FitnessAuditMixin):
    """
    Shared tenant display fields.
    """

    branch = MinimalBranchSerializer(read_only=True)
    company = MinimalCompanySerializer(read_only=True)


class TrainerCategorySerializer(FitnessAuditMixin):
    """
    Trainer category serializer.
    """

    class Meta:
        model = TrainerCategory
        fields = [
            'id', 'trainer_category_id', 'name', 'description', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'trainer_category_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault(
            'trainer_category_id', make_fitness_id('TR-CAT')
        )
        return super().create(validated_data)


class WorkoutSerializer(TenantScopedSerializer):
    """
    Workout serializer.
    """

    class Meta:
        model = Workouts
        fields = [
            'id', 'workout_id', 'body_part', 'name', 'description', 'image',
            'video', 'reps', 'sets', 'branch', 'company', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'branch', 'company', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        extra_kwargs = {
            'workout_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('workout_id', make_fitness_id('WORKOUT'))
        return super().create(validated_data)


class WorkoutPlanSerializer(TenantScopedSerializer):
    """
    Workout plan serializer.
    """

    excersises = MinimalWorkoutSerializer(many=True, read_only=True)
    excersise_ids = serializers.PrimaryKeyRelatedField(
        source='excersises',
        queryset=Workouts.objects.filter(is_active=True),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = WorkoutsPlan
        fields = [
            'id', 'workout_id', 'name', 'excersises', 'excersise_ids',
            'gender', 'difficulty', 'branch', 'company', 'is_active',
            'created_at', 'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'branch', 'company', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        extra_kwargs = {
            'workout_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('workout_id', make_fitness_id('WRK-PLAN'))
        return super().create(validated_data)


class PlaylistSerializer(TenantScopedSerializer):
    """
    Playlist serializer.
    """

    class Meta:
        model = Playlist
        fields = [
            'id', 'playlist_id', 'name', 'platform', 'decsription',
            'branch', 'company', 'is_active', 'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'branch', 'company', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        extra_kwargs = {
            'playlist_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('playlist_id', make_fitness_id('PLAYLIST'))
        return super().create(validated_data)


class PlaylistSongSerializer(FitnessAuditMixin):
    """
    Playlist song serializer.
    """

    playlist = MinimalPlaylistSerializer(read_only=True)
    playlist_id = serializers.PrimaryKeyRelatedField(
        source='playlist',
        queryset=Playlist.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = PlaylistSongs
        fields = [
            'id', 'playlist', 'playlist_id', 'songs', 'title',
            'playlist_url', 'is_active', 'created_at', 'created_by',
            'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]


class DietSerializer(TenantScopedSerializer):
    """
    Diet serializer.
    """

    class Meta:
        model = Diet
        fields = [
            'id', 'diet_id', 'name', 'descritpion', 'diet_type',
            'goal_type', 'duration', 'calorie_range', 'company', 'branch',
            'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        read_only_fields = [
            'id', 'company', 'branch', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        extra_kwargs = {
            'diet_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('diet_id', make_fitness_id('DIET'))
        return super().create(validated_data)


class ItemCategorySerializer(FitnessAuditMixin):
    """
    Food item category serializer.
    """

    class Meta:
        model = ItemCategory
        fields = [
            'id', 'item_category_id', 'name', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'item_category_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('item_category_id', make_fitness_id('ITEM-CAT'))
        return super().create(validated_data)


class ItemSerializer(FitnessAuditMixin):
    """
    Food item serializer.
    """

    category = MinimalItemCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=ItemCategory.objects.filter(is_active=True),
        write_only=True
    )
    uom = MinimalUnitOfMeasureSerializer(read_only=True)
    uom_id = serializers.PrimaryKeyRelatedField(
        source='uom',
        queryset=UnitOfMeasure.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = Item
        fields = [
            'id', 'item_id', 'name', 'category', 'category_id', 'uom',
            'uom_id', 'description', 'image', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'item_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('item_id', make_fitness_id('ITEM'))
        return super().create(validated_data)


class ItemMacrosSerializer(FitnessAuditMixin):
    """
    Food item macros serializer.
    """

    item = MinimalItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        source='item',
        queryset=Item.objects.filter(is_active=True),
        write_only=True
    )

    class Meta:
        model = ItemMacros
        fields = [
            'id', 'item_macros_id', 'item', 'item_id', 'protein', 'fat',
            'carbs', 'calories', 'sugar', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]
        extra_kwargs = {
            'item_macros_id': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('item_macros_id', make_fitness_id('MACRO'))
        return super().create(validated_data)


class DietDetailSerializer(FitnessAuditMixin):
    """
    Diet detail serializer.
    """

    diet = MinimalDietSerializer(read_only=True)
    diet_id = serializers.PrimaryKeyRelatedField(
        source='diet',
        queryset=Diet.objects.filter(is_active=True),
        write_only=True
    )
    food_items = MinimalItemSerializer(many=True, read_only=True)
    food_item_ids = serializers.PrimaryKeyRelatedField(
        source='food_items',
        queryset=Item.objects.filter(is_active=True),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = DietDetail
        fields = [
            'id', 'diet_day', 'diet', 'diet_id', 'part_of_day',
            'food_items', 'food_item_ids', 'is_active', 'created_at',
            'created_by', 'updated_at', 'updated_by'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'created_by', 'updated_at',
            'updated_by'
        ]


class MembershipPlanSerializers(TenantScopedSerializer):
    """
    Membership plan serializer.
    """

    plan_period = serializers.ChoiceField(choices=MembershipPlan.PLAN_PERIODS)
    tax_group_id = serializers.PrimaryKeyRelatedField(
        source='tax_group',
        queryset=TaxGroups.objects.filter(is_active=True),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'membershipl_plan_id', 'name', 'price', 'branch',
            'company', 'description', 'tax_group', 'tax_group_id',
            'admission_fee', 'allow_freeze', 'freeze_days', 'plan_period',
            'plan_length', 'max_sessions', 'created_at', 'updated_at',
            'is_active', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'branch', 'company', 'tax_group', 'created_at',
            'updated_at', 'is_active', 'created_by', 'updated_by'
        ]
        extra_kwargs = {
            'membershipl_plan_id': {'required': False},
            'admission_fee': {'required': False}
        }

    def create(self, validated_data):
        validated_data.setdefault('membershipl_plan_id', make_fitness_id('PLAN'))
        validated_data.setdefault('admission_fee', 0)
        return super().create(validated_data)
