from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from user.models import CustomModel
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.


# company
class Company(CustomModel):
    """
    Company or Gym Main branch.
    """

    company_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    webiste = models.URLField(max_length=256, null=True, blank=True)
    build_date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']


class CompanySettings(CustomModel):
    """
    Company configuration or settings.
    """

    company = models.OneToOneField(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='company_settings_company'
    )
    address = models.PositiveBigIntegerField()
    
    financial_year = models.PositiveBigIntegerField()
    logo = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=256)

    OWNER_STATUS = [
        ('Single Owner', 'Single Owner'),
        ('Multiple Owner', 'Multiple Owner'),
    ]
    owner_type = models.CharField(max_length=50, choices=OWNER_STATUS, null=True, blank=True)
    gstin_number = models.CharField(max_length=15, null=True, blank=True)
    currency = models.PositiveBigIntegerField()

    def __str__(self):
        return self.company.name
    
    class Meta:
        verbose_name = 'Company Settings'
        verbose_name_plural = 'Company Settings'
        ordering = ['-created_at']



# branch
class Branch(CustomModel):
    """Gym branches details."""

    branch_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    webiste = models.URLField(max_length=256, null=True, blank=True)
    build_date = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# branchsettings
class BranchSettings(CustomModel):
    """Settings for the branch"""

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name="branch_settings"
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='branch_settings_company'
    )
    address = models.PositiveBigIntegerField()
    
    is_unisex = models.BooleanField(default=True)
    GYM_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non AC', 'Non AC')
    ]
    type = models.CharField(max_length=10, null=True, blank=True, choices=GYM_TYPE_CHOICES)
    phone_number = PhoneNumberField(null=True, blank=True)

    class Meta:
        verbose_name = "Branch Settings"
        verbose_name_plural = "Branch Settings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Branch settings of {self.branch.name}"
    


class BranchTrainers(CustomModel):
    """
    Branch Trainers.
    """

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='branch_trainers_branch'
    )
    trainer = models.PositiveBigIntegerField()


    class Meta:
        verbose_name = 'Branch Trainer'
        verbose_name_plural = 'Branch Trainers'
        ordering = ['-created_at']

        


# gym working time and days:
class BranchWorkingTimeAndDays(CustomModel):
    """Branch working time and days."""

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name="branch_working_time_and_days"
    )
    am_from = models.TimeField(null=True, blank=True)
    am_to = models.TimeField(null=True, blank=True)
    pm_from = models.TimeField(null=True, blank=True)
    pm_to = models.TimeField(null=True, blank=True)
    ladies_time = models.TimeField(null=True, blank=True)
    mixed_time = models.TimeField(null=True, blank=True)

    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    working_days = models.CharField(max_length=100, choices=DAYS_OF_WEEK)
    is_holidays = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Branch Working Time and Days"
        verbose_name_plural = "Branch Working Time and Days"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.branch.name} - {self.working_days}"


# warehouse:
class Warehouse(CustomModel):
    """
    Warehouse.
    """

    warehouse_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    is_return_warehouse = models.BooleanField(default=False)

    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='company_warehouse'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='warehouse_branch'
    )
    address = models.PositiveBigIntegerField()
    account = models.PositiveBigIntegerField()

    description = CKEditor5Field('Description', config_name='extends')




class CostCenter(CustomModel):
    """
    Docstring for CostCenter
    """

    pass


class Project(CustomModel):
    """
    Docstring for Project
    """

    pass

