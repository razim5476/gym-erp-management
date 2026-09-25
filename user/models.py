"""
User models.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import random

# Create your models here.


# custom all model fields created_at, updated_at and created_by is active.
class CustomModel(models.Model):
    """custom model includes created at updated at created by is active"""

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True




# custom user mnageer:
class CustomUserManager(BaseUserManager):
    """Representing the custom base user manager."""

    def create_user(self, username, email, password=None, **extra_fields):
        """create the user"""

        if not username:
            raise ValueError("Username is required.")
        user_id = f"SUPEUSER{random.randint(1, 1000)}"
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """create a super user new."""

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)




# user model:
class User(AbstractBaseUser, PermissionsMixin):
    """Representing the users.From the abstarct base user."""

    user_id = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256)
    username = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    joined_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="users/profile/", null=True, blank=True)

    height = models.CharField(max_length=256, null=True, blank=True)
    weight = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, unique=True)

    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.ManyToManyField(
        'user.Role',
        related_name="user_role"
    )

    company = models.ForeignKey(
        'organization.Company', 
        on_delete=models.PROTECT, 
        related_name='+',
        null=True, blank=True
    )
    branch = models.ForeignKey(
        'organization.Branch', 
        on_delete=models.PROTECT, 
        related_name='+',
        null=True, blank=True
    )

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name", "email"]
    objects = CustomUserManager()



    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LoginLog(CustomModel):
    """Login log model for tracking logged in users"""

    login_log_id = models.CharField(max_length=256, unique=True)
    user = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name="login_log_user")
    description = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "Login Log"
        verbose_name_plural = "Login Logs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]



class Address(CustomModel):
    """model for storing loaction and addresses."""


    address_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(
        max_length=256, 
        help_text='For naming the address like head office or home address.'
    )
    ADDRESS_TYPES = [
        ('Head Office', 'Head Office'),
        ('Billing', 'Billing'),
        ('Shipping', 'Shipping'),
        ('Home', 'Home'),
        ('Warehouse', 'Warehouse')
    ]
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPES, null=True, blank=True)

    address_line_1 = models.CharField(max_length=256)
    address_line_2 = models.CharField(max_length=256, null=True, blank=True)
    address_line_3 = models.CharField(max_length=256, null=True, blank=True)

    city = models.CharField(max_length=256, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)

    country = models.ForeignKey('core.Country', on_delete=models.PROTECT, related_name='+')
    state = models.ForeignKey('core.State', on_delete=models.PROTECT, related_name='+')

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_address'
    )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.latitude} - {self.longitude}"




class Attendance(CustomModel):
    """model for user and trainer attendnce."""

    attendance_id = models.CharField(max_length=256, unique=True)

    attendence_for = models.CharField(max_length=50, help_text="Whose attendece like trainer, student, etc")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="attendance_user"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICE = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="Present")

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user'])
        ]

    @property
    def duration(self):
        """to check how much time a userr spend in the gym."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.start_time}"




class Role(CustomModel):
    """model for creating roles like trainer, admin, customer etc for
    the users.
    """

    role_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    descritpiton = models.CharField(max_length=256, null=True, blank=True)
    permission = models.ManyToManyField(
        'user.Permission',
        related_name="role"
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.role_id} - {self.name}"




class Permission(CustomModel):
    """model for the permission."""

    permission_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    code = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.permission_id} - {self.name}"




class UserProfile(CustomModel):
    """users profile setting"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_profile"
    )
    bio = models.TextField(null=True, blank=True)
    LEVEL_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f"{self.user.firstname} - {self.user.lastname}"




class Gallery(CustomModel):
    """model for user gallery.multiple photos."""

    user = models.ForeignKey(
        'user.UserProfile',
        on_delete=models.PROTECT,
        related_name="user_profile"
    )
    photos = models.ImageField(upload_to="")

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallerys"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f"{self.user_profile.user.firstname} {self.user_profile.user.lastname}"




# trner details:
class Trainer(CustomModel):
    """Trainer details"""

    user = models.OneToOneField(
        'user.User',
        on_delete=models.PROTECT,
        related_name="trainer_user",
    )
    experience = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    category = models.ForeignKey('core.Category', on_delete=models.PROTECT, related_name='+')
    certifiation = models.FileField(upload_to="trainer_cerfificates/")
    bio = models.TextField(null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    on_leave = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Trainer"
        verbose_name_plural = "Trainers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"
    
    
