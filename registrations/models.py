"""
Registartion Models
"""



from django.db import models
from user.models import CustomModel

# Create your models here.


class CustomerGroup(CustomModel):
    """
    Customer Group.
    """

    customer_group_id = models.CharField(max_length=256, unique=True)
    group_name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    
    company = models.PositiveBigIntegerField()
    branch = models.PositiveBigIntegerField()
    tax_group = models.PositiveBigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Customer Group'
        verbose_name_plural = 'Customer Groups'
        ordering = ['-created_at']



class Customer(CustomModel):
    """
    Customer
    """

    customer_id = models.CharField(max_length=256, unique=True)
    customer_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    customer_group = models.PositiveBigIntegerField()
    tax_group = models.PositiveBigIntegerField(null=True, blank=True)
    account = models.PositiveBigIntegerField()
    CUSTOMER_TYPES = [
        ('Company', 'Company'),
        ('Individual', 'Individual'),
        ('Partnership', 'Partnership')
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)

    website = models.URLField(null=True, blank=True)

    shipping_address = models.PositiveBigIntegerField()

    gstin = models.CharField(max_length=15, null=True, blank=True)


class SupplierGroup(CustomModel):
    """
    Docstring for Suppliergroup
    """

    pass



class Supplier(CustomModel):
    """
    Docstring for Supplier
    """

    pass
    

