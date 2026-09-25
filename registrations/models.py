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
    
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')
    tax_group = models.ForeignKey('accounts.TaxGroups', on_delete=models.PROTECT, null=True, blank=True, related_name='+')

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

    customer_group = models.ForeignKey('registrations.CustomerGroup', on_delete=models.PROTECT, related_name='+')
    tax_group = models.ForeignKey('accounts.TaxGroups', on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    account = models.ForeignKey('accounts.Accounts', on_delete=models.PROTECT, related_name='+')
    CUSTOMER_TYPES = [
        ('Company', 'Company'),
        ('Individual', 'Individual'),
        ('Partnership', 'Partnership')
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)

    website = models.URLField(null=True, blank=True)

    shipping_address = models.ForeignKey('user.Address', on_delete=models.PROTECT, related_name='+')

    tax_number = models.CharField(max_length=15, null=True, blank=True)


    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']


    def __str__(self):
        return self.customer_name
    


class SupplierGroup(CustomModel):
    """
    Docstring for Suppliergroup
    """

    supplier_group_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
        
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')
    tax_group = models.ForeignKey('accounts.TaxGroups', on_delete=models.PROTECT, null=True, blank=True, related_name='+')

    class Meta:
        verbose_name = 'Supplier Group'
        verbose_name_plural = 'Supplier Groups'
        ordering = ['-created_at']


    def __str__(self):
        return self.name
    


class Supplier(CustomModel):
    """
    Docstring for Supplier
    """

    supplier_id = models.CharField(max_length=128, unique=True)
    supplier_name = models.CharField(max_length=256)
    alias = models.CharField(max_length=120, null=True, blank=True)

    supplier_group = models.ForeignKey(
        'registrations.SupplierGroup',
        on_delete=models.PROTECT,
        related_name='supplier_group_supplier',
        null=True,
        blank=True
    )

    SUPPLIER_TYPE_CHOICE = [
        ('Company', 'Company'),
        ('Individual', 'Individual'),
        ('Partnership', 'Partnership')
    ]
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE_CHOICE)

    website = models.URLField(null=True, blank=True)
    
    address = models.ForeignKey('user.Address', on_delete=models.PROTECT, related_name='+')

    tax_number = models.CharField(max_length=15, null=True, blank=True)
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='supplier_account',
        null=True, blank=True
    )
    

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['-created_at']


    def __str__(self):
        return self.supplier_name

    
    
