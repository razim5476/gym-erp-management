"""
Docstring for accounts.urls
"""

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r'account_groups', views.AccountGroupViewSet)
router.register(r'accounts', views.AccountViewSet)


urlpatterns = router.urls