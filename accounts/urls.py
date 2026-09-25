"""
Docstring for accounts.urls
"""

from rest_framework.routers import DefaultRouter
from . import views
from django.urls import include, path


router = DefaultRouter()

router.register(r'account_groups', views.AccountGroupViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'payment_method', views.PaymentMethodViewSet, basename='payment_method')


urlpatterns = [
    path('', include(router.urls)),
    path('payment_method_dropdown/', views.PaymentMethodDropdownView.as_view(), name='payment_method_dropdown'),

]
    