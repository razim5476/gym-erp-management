"""
Tenant related models.Like the Tenant model name and domain name.
"""


from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
# Create your models here.


class Tenant(TenantMixin):
    """
    for storing Tenant name
    """

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



class Domain(DomainMixin):
    """
    for Domain storing.
    """

    pass