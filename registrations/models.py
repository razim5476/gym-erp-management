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
    
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='customer_group_company'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='customer_group_branch',
        null=True, blank=True
    )
    tax_group = models.ForeignKey(
        'accounts.TaxGroups',
        on_delete=models.PROTECT,
        related_name='customer_group_tax_group',
        null=True, blank=True
    )

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

    customer_group = models.ForeignKey(
        'registrations.CustomerGroup',
        on_delete=models.PROTECT,
        related_name='group_of_the_customer',
        null=True, blank=True
    )
    tax_group = models.ForeignKey(
        'accounts.TaxGroups',
        on_delete=models.PROTECT,
        related_name='customer_tax_group',
        null=True, blank=True
    )
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='customer_account'
    )
    CUSTOMER_TYPES = [
        ('Company', 'Company'),
        ('Individual', 'Individual'),
        ('Partnership', 'Partnership')
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)

    website = models.URLField(null=True, blank=True)

    shipping_address = models.ForeignKey(
        'user.Address',
        on_delete=models.PROTECT,
        related_name='customer_shipping_address',
        null=True, blank=True
    )

    gstin = models.CharField(max_length=15, null=True, blank=True)


class Suppliergroup(CustomModel):
    """
    Docstring for Suppliergroup
    """

    pass



class Supplier(CustomModel):
    """
    Docstring for Supplier
    """

    pass
    

