"""
Accounting Related models.
"""


from django.db import models
from django.forms import ValidationError
from user.models import CustomModel
from django.utils import timezone

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
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')


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

    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']




# bank
class Bank(CustomModel):
    """
    Bank
    """

    bank_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=100, unique=True)
    swift_code = models.CharField(max_length=50, null=True, blank=True)

    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
        ordering = ['-created_at']




class BankBranch(CustomModel):
    """
    BankBranch
    """

    bank_branch_id = models.CharField(max_length=256, unique=True)
    bank = models.ForeignKey(
        'accounts.Bank',
        on_delete=models.PROTECT,
        related_name='bank_branch_bank'
        )
    name = models.CharField(max_length=256)
    swift_code = models.CharField(max_length=20, unique=True)
    address = models.ForeignKey('user.Address', on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return f"{self.bank.name} - {self.name}"
    
    class Meta:
        verbose_name = 'Bank Branch'
        verbose_name_plural = 'Bank Branches'
        ordering = ['-created_at']



class BankAccountType(CustomModel):
    """
    Bank account types
    Like: Savings, Current etc.
    """

    bank_account_type_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = 'Bank Account Type'
        verbose_name_plural = 'Bank Account Types'
        ordering = ['-created_at']


    def __str__(self):
        return self.name



class BankAccount(CustomModel):
    """
    BankAccount
    """

    bank_account_id = models.CharField(max_length=256, unique=True)
    bank_branch = models.ForeignKey(
        'accounts.BankBranch',
        on_delete=models.PROTECT,
        related_name='bank_account_bank_branch'
    )
    account = models.OneToOneField(
        'accounts.Accounts',
        on_delete=models.CASCADE,
        related_name='bank_details',

    )
    bank_account_type = models.ForeignKey(
        'accounts.BankAccountType',
        on_delete=models.PROTECT,
        related_name='bank_account_type_account',
        null=True, blank=True
    )

    account_no = models.CharField(max_length=50, unique=True)

    ACCOUNT_TYPE = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
        ('Fixed', 'Fixed'),
    ]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)

    ## party details like what if customer or employee or supplier bank
    PARTY_TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('Supplier', 'Supplier'),
        ('Employee', 'Employee')
    ]
    party_type = models.CharField(max_length=20, choices=PARTY_TYPE_CHOICES, null=True, blank=True)
    customer = models.ForeignKey(
        'registrations.Customer',
        on_delete=models.PROTECT,
        related_name='bank_account_customer',
        null=True,
        blank=True
    )
    supplier = models.ForeignKey(
        'registrations.Supplier',
        on_delete=models.PROTECT,
        related_name='bank_account_supplier',
        null=True,
        blank=True
    )

    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    contact_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.CharField(max_length=50, null=True, blank=True)

    is_default = models.BooleanField(default=False)
    is_company_account = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'
        ordering = ['-created_at']

    def clean(self):
        if self.account.sub_type != 'Bank':
            raise ValidationError(
                "BankAccountDetails can only be linked to accounts with sub_type='Bank'"
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()   # ensures clean() is always called
        super().save(*args, **kwargs)



class TaxType(CustomModel):
    """
    Tax types
    Like: GST, VAT
    """

    tax_type_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256, unique=True)



# tax
class Tax(CustomModel):
    """
    Taxes

    Like:
        IGST 10%
    """

    tax_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)

    tax_type = models.ForeignKey(
        'accounts.TaxType',
        on_delete=models.PROTECT,
        related_name='tax_taxtype',
    )
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='tax_account'
    )
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

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
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tax Groups'
        verbose_name_plural = 'Tax Groups'
        ordering = ['-created_at']



class TaxGroupDetail(CustomModel):
    """
    Tax Group Detail
    """

    tax_group = models.ForeignKey(
        'accounts.TaxGroups',
        on_delete=models.PROTECT,
        related_name='tax_group_details'
    )
    tax = models.ForeignKey(
        'accounts.Tax',
        on_delete=models.PROTECT,
        related_name='tax_groups_tax'
    )
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = 'Tax Group Detail'
        verbose_name_plural = 'Tax Group Details'
        ordering = ['-created_at']

    def __str__(self):
        return self.tax_group.name


class GeneralLedger(CustomModel):
    """
    General ledger.
    """

    gl_id = models.CharField(max_length=256, unique=True)
    voucher_no = models.CharField(max_length=256, db_index=True)

    # account currency:
    debit_amount_ac = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Debit amount in account currency"
    )
    credit_amount_ac = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Credit amount in account currency"
    )
    account_currency = models.ForeignKey('core.Currency', on_delete=models.PROTECT, related_name='+')

    # trannsaction currency:
    debit_amount_tc = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Debit amount in transaction currency"
    )
    credit_amount_tc = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Credit amount in transaction currency"
    )
    transaction_currency = models.ForeignKey('core.Currency', on_delete=models.PROTECT, related_name='+')

    # company default currency:
    debit_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Debit amount in base currency"
    )
    credit_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0,
        help_text="Credit amount in base currency"
    )
    
    # Exchange rates
    transaction_exchange_rate = models.DecimalField(
        max_digits=12, decimal_places=6, default=1,
        help_text="Exchange rate: Transaction Currency to Base Currency(Company default currency)"
    )
    account_exchange_rate = models.DecimalField(
        max_digits=12, decimal_places=6, default=1,
        help_text="Exchange rate: Account Currency to Base Currency(Company default currency)"
    )

    posting_date = models.DateField(default=timezone.localdate)
    transaction_datetime = models.DateTimeField(auto_now_add=True)

    fiscal_year = models.CharField(max_length=10, null=True, blank=True)
    fiscal_period = models.CharField(max_length=10, null=True, blank=True)

    customer = models.ForeignKey(
        'registrations.Customer', 
        on_delete=models.PROTECT, 
        related_name='general_ledger_customer', 
        null=True, 
        blank=True
    )
    supplier = models.ForeignKey(
        'registrations.Supplier',
        on_delete=models.PROTECT, 
        related_name='general_ledger_supplier', 
        null=True, 
        blank=True
    )
    
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='gl_account'
    )
    against_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='gl_against_account'
    )
    
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    PARTY_STATUS = [
        ('Customer', 'Customer'),
        ('Supplier', 'Supplier')
    ]
    party_type = models.CharField(choices=PARTY_STATUS, null=True, blank=True)
    VOUCHER_TYPE = [
        ('Purchase Invoice', 'Purchase Invoice'),
        ('Sale Invoice', 'Sale Invoice'),
    ]
    voucher_type = models.CharField(max_length=256, choices=VOUCHER_TYPE)
    voucher_sub_type = models.CharField(max_length=256, null=True, blank=True)
    against_voucher = models.CharField(max_length=256, null=True, blank=True)
    against_voucher_type = models.CharField(max_length=256, null=True, blank=True)

    is_cancelled = models.BooleanField(default=False)
    is_reconciled = models.BooleanField(default=False)

    remarks = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = "General Ledger Entry"
        verbose_name_plural = "General Ledger Entries"
        ordering = ['-posting_date', '-transaction_datetime']
        
        indexes = [
            models.Index(fields=['voucher_no', 'posting_date']),
            models.Index(fields=['account', 'posting_date']),
            models.Index(fields=['company', 'posting_date']),
            models.Index(fields=['is_cancelled']),
        ]

    


class Journal(CustomModel):
    """
    Docstring for Journal
    """

    journal_id = models.CharField(max_length=256, unique=True)
    posting_date = models.DateTimeField()

    ENTRY_TYPES = [
        ('Journal Entry', 'Journal Entry'),
        ('Bank Entry', 'Bank Entry'),
        ('Cash Entry', 'Cash Entry'),
        ('Opening Entry', 'Opening Entry')
    ]
    entry_type = models.CharField(choices=ENTRY_TYPES, max_length=20)

    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    total_debit_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        help_text="Total debit in transaction currency"
    )
    total_credit_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        help_text="Total credit in transaction currency"
    )

    total_debit_in_company_currency = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        help_text="Total debit in company currency"
    )
    total_credit_in_company_currency = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        help_text="Total credit in company currency"
    )

    difference_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        default=0,
        help_text="Exchange gain/loss amount"
    )


    reference_number = models.CharField(max_length=256, null=True, blank=True)
    reference_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    is_opening = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    multi_currency = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = 'Journals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['journal_id']),
            models.Index(fields=['posting_date']),
        ]

    
    def __str__(self):
        return self.journal_id





class JournalDetails(CustomModel):
    """
    Docstring for JournalDetails
    """

    journal = models.ForeignKey(
        'accounts.Journal',
        on_delete=models.PROTECT,
        related_name='journal_details_journal'
    )
    row_index = models.PositiveIntegerField()
    
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='journal_details_account'
    )
    account_currency = models.ForeignKey('core.Currency', on_delete=models.PROTECT, related_name='+')

    PARTY_TYPE = [
        ('Supplier', 'Supplier'),
        ('Customer', 'Customer'),
        ('Employee', 'Employee')
    ]
    party_type = models.CharField(choices=PARTY_TYPE, max_length=20, null=True, blank=True)


    customer = models.ForeignKey('registrations.Customer', on_delete=models.PROTECT, related_name='+')
    supplier = models.ForeignKey('registrations.Supplier', on_delete=models.PROTECT, related_name='+')
    employee = models.ForeignKey('hr.Employee', on_delete=models.PROTECT, related_name='+')

    debit_amount = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)

    exchange_rate = models.DecimalField(
        max_digits=15, 
        decimal_places=6, 
        default=1.0,
        help_text="Exchange rate from account currency to company currency"
    )

    debit_amount_in_company_currency = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        null=True, 
        blank=True,
        help_text="Debit amount in company currency"
    )
    credit_amount_in_company_currency = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        null=True, 
        blank=True,
        help_text="Credit amount in company currency"
    )


    class Meta:
        verbose_name = 'Journal Details'
        verbose_name_plural = 'Journal Details'
        ordering = ['-created_at']
        unique_together = [['journal', 'row_index']]
        indexes = [
            models.Index(fields=['journal', 'row_index']),
            models.Index(fields=['account']),
            models.Index(fields=['account_currency']),
        ]

    
    def __str__(self):
        return self.journal.journal_id
    




class OpeningInvoiceCreation(CustomModel):
    """
    For creating invoice from the old software to new software.
    """

    opening_invoice_id = models.CharField(max_length=256, unique=True)
    posting_date = models.DateTimeField()

    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')
    
    INVOICE_TYPE = [
        ('Sale', 'Sale'),
        ('Purchase', 'Purchase'),
        ('Service', 'Service')
    ]
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPE)

    cost_center = models.ForeignKey('organization.CostCenter', on_delete=models.PROTECT, related_name='+')
    project = models.ForeignKey('organization.Project', on_delete=models.PROTECT, related_name='+')

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Submitted', 'Submitted'),
        ('Cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    remarks = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = 'Opening Invoice Creation'
        verbose_name_plural = 'Opening Invoice Creations'
        ordering = ['-posting_date', '-created_at']
        indexes = [
            models.Index(fields=['opening_invoice_id']),
            models.Index(fields=['invoice_type']),
            models.Index(fields=['posting_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.opening_invoice_id
    




class OpeningInvoiceCreationItems(CustomModel):
    """
    Docstring for OpeningInvoiceCreationItems
    """

    opening_invoice = models.ForeignKey(
        'accounts.OpeningInvoiceCreation',
        on_delete=models.CASCADE,
        related_name='opening_invoice_items'
    )

    customer = models.ForeignKey('registrations.Customer', on_delete=models.PROTECT, related_name='+')
    supplier = models.ForeignKey('registrations.Supplier', on_delete=models.PROTECT, related_name='+')

    invoice_number = models.CharField(
        max_length=256, 
        null=True, 
        blank=True,
        help_text="Original invoice number from previous system"
    )

    posting_date = models.DateField()
    due_date = models.DateField()

    item_name = models.CharField(max_length=256, default='Opening Invoice')
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=5)
    row_index = models.PositiveIntegerField()


    class Meta:
        verbose_name = 'Opening Invoice Creation Items'
        verbose_name_plural = 'Opening Invoice Creation Items'
        ordering = ['opening_invoice', 'row_index']
        unique_together = [['opening_invoice', 'row_index']]
        indexes = [
            models.Index(fields=['opening_invoice', 'row_index']),
            models.Index(fields=['customer']),
            models.Index(fields=['supplier']),
            models.Index(fields=['posting_date']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return self.opening_invoice.opening_invoice_id
    


class PaymentMethod(CustomModel):
    """
    Payment Method
    """

    payment_method_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='payment_method_account'
    )
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)

    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Method'
        ordering = ['-created_at']




class DefaultAccount(CustomModel):
    """
    Default Account
    """

    default_account_id = models.CharField(max_length=128, unique=True)

    default_bank_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_bank',
        null=True,
        blank=True
    )
    default_cogs_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_cogs'
    )
    default_income_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_income'
    )
    default_write_off_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_write_off'
    )
    default_round_off_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_round_off'
    )
    default_stock_adjustment_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_stock_adjustment'
    )
    default_stock_received_but_not_billed = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_stock_receievd_not_billed'
    )
    default_stock_account = models.ForeignKey(
        'accounts.Accounts',
        on_delete=models.PROTECT,
        related_name='default_stock_account'
    )

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='default_branch'
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='default_company'
    )


    class Meta:
        verbose_name = 'Default Account'
        verbose_name_plural = 'Default Accounts'
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.branch} - {self.company}"

    

    