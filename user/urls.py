"""
Urls for the user app.
"""
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user_view')

urlpatterns = [
    path('', include(router.urls)),
    path('user_login/', views.UserLoginView.as_view(), name='user_login'),
    path('user_registration/', views.RegisterUserView.as_view(), name='user_registration'),
]
