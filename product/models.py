"""
Product
"""

from django.db import models
from user.models import CustomModel
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.



# product catrgory:
class ProductCategory(CustomModel):
    """
    Product Categories
    """

    product_category_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=50, unique=True)
    tax_group = models.PositiveBigIntegerField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='product_category_parent',
        null=True, blank=True
    )

    hsn_code = models.CharField(max_length=50, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    description = CKEditor5Field('Description', config_name="extends")


    def __str__(self):
        return self.name
    

# product:
class Products(CustomModel):
    """
    Product
    """

    product_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    product_group = models.ForeignKey(
        'product.ProductCategory',
        on_delete=models.PROTECT,
        related_name='product_group',
        null=True, blank=True
    )
    default_uom = models.PositiveBigIntegerField()

    has_variants = models.BooleanField(default=False)
    maintain_stock = models.BooleanField(default=True)
    is_template = models.BooleanField(default=False)
    description = CKEditor5Field('Description', config_name="extends")

    opening_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valuation_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    expiry_date = models.DateField(null=True, blank=True)
    VALUATION_CHOICES = [
        ('FIFO', 'FIFO'),
        ('LIFO', 'LIFO'),
        ('Moving Average', 'Moving Average')
    ]
    valuation_method = models.CharField(max_length=50, choices=VALUATION_CHOICES)

    barcode = models.CharField(max_length=256, unique=True, null=True, blank=True)
    barcode_type = models.PositiveBigIntegerField()
    hsn_code = models.CharField(max_length=256)

    allow_sale = models.BooleanField(default=True)
    allow_purchase = models.BooleanField(default=True)

    default_warehouse = models.PositiveBigIntegerField()

    image = models.URLField(null=True, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mop = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    brand = models.PositiveBigIntegerField()
    variant = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='product_variant',
        null=True, blank=True
    )
    tax_group = models.PositiveBigIntegerField()
    default_sales_uom = models.PositiveBigIntegerField()
    default_purchase_uom = models.PositiveBigIntegerField()

    is_warranty = models.BooleanField(default=False)
    warranty_period = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['product_id']),
        ]

    
class ProductUOMs(CustomModel):
    """
    Product UOM with conversion factor.
    """

    product = models.ForeignKey(
        'product.Products',
        on_delete=models.PROTECT,
        related_name='product_uoms'
    )
    from_uom = models.ForeignKey(
        'core.UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='from_uom'
    )
    to_uom = models.ForeignKey(
        'core.UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='to_uom'
    )

    conversion_factor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Product UOM',
        verbose_name_plural = 'Product UOMs'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'from_uom', 'to_uom'],
                name='unique_product_uom_conversion'
            )
        ]


# product bundle:
class ProductsBundle(CustomModel):
    """
    Products Bundles
    """

    product_bundle_id = models.CharField(max_length=256, unique=True)
    template_product = models.ForeignKey(
        'product.Products',
        on_delete=models.PROTECT,
        related_name='template_product',
        limit_choices_to={'is_template': True, 'allow_sale': True}
    )
    description = CKEditor5Field('Description', config_name='extends')

    def __str__(self):
        return self.template_product
    
    class Meta:
        verbose_name = 'Product Bundle'
        verbose_name_plural = 'Product Bundles'
        ordering = ['-created_at']


class ProductBundleItems(CustomModel):
    """
    Product bundle items
    """

    product_bundle = models.ForeignKey(
        'product.ProductsBundle',
        on_delete=models.PROTECT,
        related_name='product_bundle_parent'
    )
    product = models.ForeignKey(
        'product.Products',
        on_delete=models.PROTECT,
        related_name='product_bundle_product'
    )
    quantity = models.PositiveIntegerField(default=1)
    uom = models.ForeignKey(
        'core.UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='product_bundle_uom'
    )
    line_no = models.PositiveIntegerField()

    def __str__(self):
        return self.product_bundle.template_product

    class Meta:
        verbose_name = 'Product Bundle Item'
        verbose_name_plural = 'Product Bundle Items'
        ordering = ['-created_at']


class ProductAttributes(CustomModel):
    """
    Product Attributes
    """

    product_attribute_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    is_numeric_values = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Attribute'
        verbose_name_plural = 'Product Attributes'
        ordering = ['-created_at']


class ProductAttributeValues(CustomModel):
    """
    Product Attribute Values
    """

    product_attribute = models.ForeignKey(
        'product.ProductAttributes',
        on_delete=models.PROTECT,
        related_name='attribute_values'
    )
    value = models.CharField(max_length=256, null=True, blank=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    line_no = models.PositiveBigIntegerField(null=True, blank=True)

    from_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    to_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    increment = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        if self.value:
            return f"{self.product_attribute.name}: {self.value}"
        elif self.from_range and self.to_range:
            return f"{self.product_attribute.name}: {self.from_range} - {self.to_range}"
        return self.product_attribute.name
    
    class Meta:
        verbose_name = 'Product Attribute Value'
        verbose_name_plural = 'Product Attributes Values'
        ordering = ['-created_at']


class ProductVariantAttribute(CustomModel):
    """
    Product Variant Attributes
    """

    product = models.ForeignKey(
        'product.Products',
        on_delete=models.PROTECT,
        related_name='product_variant_attributes',
        limit_choices_to={'is_variant': True}
    )
    company = models.PositiveBigIntegerField()
    branch = models.PositiveBigIntegerField()
    


