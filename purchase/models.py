"""
Purchase related models
"""


from django.db import models

from user.models import CustomModel

# Create your models here.



class PurchaseOrder(CustomModel):
    """
    PurchaseOrder
    """

    purchase_order_id = models.CharField(max_length=256, unique=True)
    date = models.DateField()
    required_by = models.DateField(null=True, blank=True)

    supplier = models.PositiveBigIntegerField()
    cost_center = models.PositiveBigIntegerField()
    project = models.PositiveBigIntegerField()
    currency = models.PositiveBigIntegerField()
    warehouse = models.PositiveBigIntegerField()
    tax_group = models.PositiveBigIntegerField(null=True, blank=True)

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
        related_name='purchase_order_payment_term'
    )

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.purchase_order_id
    

    

