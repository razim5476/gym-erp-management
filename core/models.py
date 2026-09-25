from django.db import models
from user.models import CustomModel
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.


# state:
class State(CustomModel):
    """States"""

    state_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    country = models.ForeignKey(
        'core.Country',
        on_delete=models.PROTECT,
        related_name="states"
    )

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_state_in_country')
        ]

    def __str__(self):
        return self.name


# coutnry:
class Country(CustomModel):
    """Country."""

    country_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['created_at']

    def __str__(self):
        return self.name


# currency:
class Currency(CustomModel):
    """
    Currency.
    """

    currency_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ['-created_at']



# uom
class UnitOfMeasure(CustomModel):
    """Unit of measure"""

    uom_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(unique=True, max_length=20)
    short_name = models.CharField(unique=True, max_length=5)

    class Meta:
        verbose_name = "Unit Of Measure"
        verbose_name_plural = "Unit Of Measures"
        ordering = ['-created_at']


class Brand(CustomModel):
    """
    Brand.
    """

    brand_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    description = CKEditor5Field('Description', config_name='extends')
    
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['-created_at']



class Category(CustomModel):
    """
    Category.
    """

    category_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    description = CKEditor5Field('Description', config_name='extends')
    
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']


class SubCategory(CustomModel):
    """
    SubCategory
    """

    sub_category_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey('core.Category', on_delete=models.PROTECT, related_name='+')
    description = CKEditor5Field('Description', config_name='extends')
    
    company = models.ForeignKey('organization.Company', on_delete=models.PROTECT, related_name='+')
    branch = models.ForeignKey('organization.Branch', on_delete=models.PROTECT, related_name='+')

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        ordering = ['-created_at']



class Barcodes(CustomModel):
    """
    Barcode.
    """

    barcode_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = CKEditor5Field('Description', config_name='extends')

    class Meta:
        verbose_name = 'Barcode'
        verbose_name_plural = 'Barcodes'
        ordering = ['-created_at']



class PaginationSize(CustomModel):
    """
    Docstring for Pgaination.Per page data limit or size.
    """

    pagination_id = models.CharField(max_length=256, unique=True)
    data_per_page = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = 'Pagination Size'
        verbose_name_plural = 'Pagination Sizes'
        ordering = ['-created_at']

    def __str__(self):
        return self.data_per_page
    


class UniqueId(CustomModel):
    """
    Unique id storing for each model.
    """

    prefix = models.CharField(max_length=20)
    unique_id = models.PositiveBigIntegerField(default=1)
    model = models.CharField(max_length=20)
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='unique_id_branch'
    )

    class Meta:
        verbose_name = 'UniqueId'
        verbose_name_plural = 'UniqueIds'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['model', 'prefix', 'branch'],
                name='unique_id_per_model_prefix_branch'
            )
        ]

    def __str__(self):
        return f"{self.prefix} - {self.model}"



class FinancialYear(CustomModel):
    """
    Financial Year
    """

    financial_year_id = models.CharField(max_length=256, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()


    class Meta:
        verbose_name = 'Financial Year'
        verbose_name_plural = 'Financial Years'
        ordering = ['-created_at']

        
