"""
Purchase related models
"""


from django.db import models
from user.models import CustomModel

# Create your models here.



class Purchase(CustomModel):
    """
    PurchaseOrder
    """

    purchase_id = models.CharField(max_length=256, unique=True)
    date = models.DateField()
    required_by = models.DateField(null=True, blank=True)

    supplier = models.ForeignKey('registrations.Supplier', on_delete=models.PROTECT, related_name='+')
    cost_center = models.ForeignKey('organization.CostCenter', on_delete=models.PROTECT, related_name='+')
    project = models.ForeignKey('organization.Project', on_delete=models.PROTECT, related_name='+')
    currency = models.ForeignKey('core.Currency', on_delete=models.PROTECT, related_name='+')
    warehouse = models.ForeignKey('organization.Warehouse', on_delete=models.PROTECT, related_name='+')
    tax_group = models.ForeignKey('accounts.TaxGroups', on_delete=models.PROTECT, null=True, blank=True, related_name='+')

    total_quantity = models.PositiveIntegerField(default=1)
    total_price_without_tax = models.DecimalField(max_digits=15, decimal_places=2)

    grand_total = models.DecimalField(max_digits=15, decimal_places=5)
    rounding_adjustment = models.DecimalField(max_digits=15, decimal_places=5)

    rounded_total = models.DecimalField(max_digits=15, decimal_places=2)
    advance_paid = models.DecimalField(max_digits=15, decimal_places=5)

    # discount:
    DISCOUNT_STATUS = [
        ('Grand Total', 'Grand Total'),
        ('Net Total', 'Net Total')
    ]
    discount_on = models.CharField(max_length=20, choices=DISCOUNT_STATUS)
    discount_percentage = models.PositiveIntegerField()
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2)

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Order Placed', 'Order Placed')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    # payment terms and conditons:
    payment_terms = models.ForeignKey(
        'core.PaymentTerms',
        on_delete=models.PROTECT,
        related_name='purchase_payment_term'
    )

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchase'
        ordering = ['-created_at']

    def __str__(self):
        return self.purchase_id
    

    

