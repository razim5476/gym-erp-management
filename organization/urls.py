"""
Urls and router s for the organization app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('branch-with-settings', views.BranchSettingsView.as_view(), name='branch-with-settings')
]
