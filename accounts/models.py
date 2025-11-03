"""
Accounting Related models.
"""


from django.db import models
from user.models import CustomModel

# Create your models here.


# accoun groups
class AccountGroups(CustomModel):
    """
    Account groups.
    """

    group_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='child_groups',
        null=True, blank=True
    )
    level = models.PositiveIntegerField(default=1)
    ACCOUNT_GROUP_TYPES = [
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Equity', 'Equity')
    ]
    root_type = models.CharField(max_length=10, choices=ACCOUNT_GROUP_TYPES, null=True, blank=True)
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='account_groups_company'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Account Groups'
        verbose_name_plural = 'Account Groups'
        ordering = ['-created_at']


# acounts
class Accounts(CustomModel):
    """
    Accounts
    """

    account_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)

    account_group = models.ForeignKey(
        'accounts.AccountGroups',
        on_delete=models.PROTECT,
        related_name='accounts_group'
    )
    currency = models.ForeignKey(
        'core.Currency',
        on_delete=models.PROTECT,
        related_name='accounts_currency'
    )

    ACCOUNT_SUB_TYPES = [
        ('Cash', 'Cash'),
        ('Accounts Payable', 'Accounts Payable'),
        ('Accounts Receivable', 'Accounts Receivable'),
        ('Bank', 'Bank')
    ]
    sub_type = models.CharField(max_length=50, choices=ACCOUNT_SUB_TYPES)

    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='accounts_company',
        null=True, blank=True
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='account_branch',
        null=True, blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']


# bank
class Bank(models.Model):
    """
    Bank
    """

    bank_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    branch_name = models.CharField(max_length=256)

    account_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    BANK_ACCOUNT_TYPE = [
        ('Savings', 'Savings'),
        ('Currenct', 'Current'),
        ('Fixed', 'Fixed')
    ]
    bank_account_type = models.CharField(max_length=50, choices=BANK_ACCOUNT_TYPE, null=True, blank=True)
    ifsc_code = models.CharField(max_length=50, null=True, blank=True)
    swift_code = models.CharField(max_length=50, null=True, blank=True)

    address = models.ForeignKey(
        'user.Address',
        on_delete=models.PROTECT,
        related_name='bank_address',
        null=True, blank=True
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='company_bank',
        null=True, blank=True
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='bank_branch',
        null=True, blank=True
    )

    contact_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.CharField(max_length=50, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
        ordering = ['-created_at']




# tax
class Tax(CustomModel):
    """
    Taxes

    Like:
        IGST 10%
    """

    tax_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='tax_company'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='tax_branch',
        null=True, blank=True
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'
        ordering = ['-created_at']


# tax groups
class TaxGroups(CustomModel):
    """
    Tax Groups

    Like:
        GST 10%
    """

    tax_group_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    
    tax = models.ForeignKey(
        'accounts.Tax',
        on_delete=models.PROTECT,
        related_name='tax_groups_tax'
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='tax_group_company'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='tax_branch',
        null=True, blank=True
    )

    tax_rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tax Groups'
        verbose_name_plural = 'Tax Groups'
        ordering = ['-created_at']


