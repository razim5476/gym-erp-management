from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from user.models import CustomModel
from django.utils import timezone
# Create your models here.


# branch
class Branch(CustomModel):
    """Gym branches details."""

    branch_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.ForeignKey(
        'core.Country',
        on_delete=models.PROTECT,
        related_name="branch_country"
    )
    state = models.ForeignKey(
        'core.State',
        on_delete=models.PROTECT,
        related_name="branch_state"
    )
    location = models.CharField(max_length=50)
    address_line = models.CharField(max_length=256)
    address_line_2 = models.CharField(max_length=256, null=True, blank=True)
    address_line_3 = models.CharField(max_length=256, null=True, blank=True)
    pincode = models.IntegerField()

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
    trainers = models.ManyToManyField(
        'user.Trainer',
        related_name="branch_trainers"
    )
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


# gym
class Gym(CustomModel):
    """Gym details."""

    gym_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=50, unique=True)
    GYM_TYPE = [
        ('Partnership', 'Partnership'),
        ('Own', 'Own')
    ]
    type = models.CharField(max_length=50, choices=GYM_TYPE)
    owner_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Gym"
        verbose_name_plural = "Gyms"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


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
