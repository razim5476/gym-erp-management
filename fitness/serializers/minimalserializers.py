"""
Fitness minimal serializers.
"""

from rest_framework import serializers

from fitness.models import (
    Diet,
    Item,
    ItemCategory,
    MembershipPlan,
    Playlist,
    TrainerCategory,
    Workouts,
    WorkoutsPlan,
)


class MinimalTrainerCategorySerializer(serializers.ModelSerializer):
    """
    Minimal trainer category serializer.
    """

    class Meta:
        model = TrainerCategory
        fields = ['id', 'trainer_category_id', 'name']


class MinimalWorkoutSerializer(serializers.ModelSerializer):
    """
    Minimal workout serializer.
    """

    class Meta:
        model = Workouts
        fields = ['id', 'workout_id', 'name', 'body_part']


class MinimalWorkoutPlanSerializer(serializers.ModelSerializer):
    """
    Minimal workout plan serializer.
    """

    class Meta:
        model = WorkoutsPlan
        fields = ['id', 'workout_id', 'name', 'gender', 'difficulty']


class MinimalPlaylistSerializer(serializers.ModelSerializer):
    """
    Minimal playlist serializer.
    """

    class Meta:
        model = Playlist
        fields = ['id', 'playlist_id', 'name', 'platform']


class MinimalDietSerializer(serializers.ModelSerializer):
    """
    Minimal diet serializer.
    """

    class Meta:
        model = Diet
        fields = ['id', 'diet_id', 'name', 'diet_type', 'goal_type']


class MinimalItemCategorySerializer(serializers.ModelSerializer):
    """
    Minimal item category serializer.
    """

    class Meta:
        model = ItemCategory
        fields = ['id', 'item_category_id', 'name']


class MinimalItemSerializer(serializers.ModelSerializer):
    """
    Minimal food item serializer.
    """

    class Meta:
        model = Item
        fields = ['id', 'item_id', 'name']


class MinimalMembershipPlanSerializer(serializers.ModelSerializer):
    """
    Minimal membership plan serializer.
    """

    class Meta:
        model = MembershipPlan
        fields = [
            'id', 'membershipl_plan_id', 'name', 'plan_period',
            'plan_length', 'price', 'admission_fee', 'max_sessions'
        ]
