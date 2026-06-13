"""
User URLs.
"""

from rest_framework.routers import DefaultRouter

from user import views


router = DefaultRouter()

router.register(r'membership', views.MembershipViewSet, basename='membership')

urlpatterns = router.urls
