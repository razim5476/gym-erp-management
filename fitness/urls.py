"""
Fitness urls.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from fitness import views


router = DefaultRouter()

router.register(
    r'trainer_categories',
    views.TrainerCategoryViewSet,
    basename='trainer-category'
)
router.register(
    r'trainer_category_dropdown',
    views.TrainerCategoryDropdownViewSet,
    basename='trainer-category-dropdown'
)
router.register(r'workouts', views.WorkoutViewSet, basename='workout')
router.register(
    r'workout_dropdown',
    views.WorkoutDropdownViewSet,
    basename='workout-dropdown'
)
router.register(
    r'workout_plans',
    views.WorkoutPlanViewSet,
    basename='workout-plan'
)
router.register(
    r'workout_plan_dropdown',
    views.WorkoutPlanDropdownViewSet,
    basename='workout-plan-dropdown'
)
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(
    r'playlist_dropdown',
    views.PlaylistDropdownViewSet,
    basename='playlist-dropdown'
)
router.register(
    r'playlist_songs',
    views.PlaylistSongViewSet,
    basename='playlist-song'
)
router.register(r'diets', views.DietViewSet, basename='diet')
router.register(
    r'diet_dropdown',
    views.DietDropdownViewSet,
    basename='diet-dropdown'
)
router.register(r'diet_details', views.DietDetailViewSet, basename='diet-detail')
router.register(
    r'item_categories',
    views.ItemCategoryViewSet,
    basename='item-category'
)
router.register(
    r'item_category_dropdown',
    views.ItemCategoryDropdownViewSet,
    basename='item-category-dropdown'
)
router.register(r'items', views.ItemViewSet, basename='item')
router.register(
    r'item_dropdown',
    views.ItemDropdownViewSet,
    basename='item-dropdown'
)
router.register(r'item_macros', views.ItemMacrosViewSet, basename='item-macros')
router.register(
    r'membership_plans',
    views.MembershipPlanViewSet,
    basename='membership-plan'
)
router.register(
    r'membership_dropdown',
    views.MembershipPlanDropdown,
    basename='membership-dropdown'
)

urlpatterns = [
    path('', include(router.urls)),
]
