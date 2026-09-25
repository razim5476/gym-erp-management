"""
User URLs.
"""

from django.urls import path

from user import views


urlpatterns = [
    path("users/", views.UserAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserAPIView.as_view(), name="user-detail"),

    path("membership/", views.MembershipAPIView.as_view(), name="membership-list"),
    path(
        "membership/<int:pk>/",
        views.MembershipAPIView.as_view(),
        name="membership-detail",
    ),

    path("login-logs/", views.LoginLogAPIView.as_view(), name="login-log-list"),
    path(
        "login-logs/<int:pk>/",
        views.LoginLogAPIView.as_view(),
        name="login-log-detail",
    ),

    path("addresses/", views.AddressAPIView.as_view(), name="address-list"),
    path(
        "addresses/<int:pk>/",
        views.AddressAPIView.as_view(),
        name="address-detail",
    ),

    path("attendances/", views.AttendanceAPIView.as_view(), name="attendance-list"),
    path(
        "attendances/<int:pk>/",
        views.AttendanceAPIView.as_view(),
        name="attendance-detail",
    ),

    path("roles/", views.RoleAPIView.as_view(), name="role-list"),
    path("roles/<int:pk>/", views.RoleAPIView.as_view(), name="role-detail"),

    path("permissions/", views.PermissionAPIView.as_view(), name="permission-list"),
    path(
        "permissions/<int:pk>/",
        views.PermissionAPIView.as_view(),
        name="permission-detail",
    ),

    path("profiles/", views.UserProfileAPIView.as_view(), name="profile-list"),
    path(
        "profiles/<int:pk>/",
        views.UserProfileAPIView.as_view(),
        name="profile-detail",
    ),

    path("galleries/", views.GalleryAPIView.as_view(), name="gallery-list"),
    path(
        "galleries/<int:pk>/",
        views.GalleryAPIView.as_view(),
        name="gallery-detail",
    ),

    path("trainers/", views.TrainerAPIView.as_view(), name="trainer-list"),
    path(
        "trainers/<int:pk>/",
        views.TrainerAPIView.as_view(),
        name="trainer-detail",
    ),
]
