"""
organizations urls
"""

from rest_framework.routers import DefaultRouter
from .views import CompanyCreateViewSet
from django.urls import path, include

router = DefaultRouter()



urlpatterns = [
    path('company-create/', CompanyCreateViewSet.as_view(), name='company-create'),
    path('', include(router.urls))
]
