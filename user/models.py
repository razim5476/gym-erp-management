from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


# custom all model fields created_at, updated_at and created_by is active.
class CustomModel(models.Model):
    """custom model includes created at updated at created by is active"""

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_%(class)s_objects")
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# custom user mnageer:
class CustomUserManager(BaseUserManager):
    """Representing the custom base user manager."""

    def create_user(self, email, passoword=None, **extra_fields):
        """create the user"""

        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(passoword)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """create a super user new."""

        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


# user model:
class User(AbstractBaseUser):
    """Representing the users.From the abstarct base user."""

    user_id = models.CharField(max_length=256, unique=True)
    firstname = models.CharField(max_length=256, null=True, blank=True)
    lastname = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    joined_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="", null=True, blank=True)
    USER_TYPE_CHOICES = [
        ('Branch Admin', 'Branch Admin'),
        ('Trainer', 'Trainer'),
        ('Member', 'Member')
    ]
    userr_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_trainer = models.BooleanField(default=False)
    height = models.CharField(max_length=256, null=True, blank=True)
    weight = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.OneToOneField(
        'user.Address',
        on_delete=models.PROTECT,
        related_name="user_address",
        null=True,
        blank=True
    )
    role = models.ForeignKey(
        'user.Role',
        on_delete=models.PROTECT,
        related_name="user_role"
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='company_user'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='branch_user'
    )

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    @property
    def is_trainer(self):
        return self.userr_type == "Trainer"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


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


class ActivityLog(CustomModel):
    """activity log model for logging the actvity done by each user.like create, udate or delete
    on model level.
    """

    activity_log_id = models.CharField(max_length=256, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="activity_log_user")
    module_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=100)
    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    ]
    action_type = models.CharField(max_length=50, null=True, blank=True, choices=ACTION_CHOICES)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    request_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action_type} on {self.module_name}"


class Address(CustomModel):
    """model for storing loaction and addresses."""


    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    content_object = GenericForeignKey(
        'content_type', 'object_id'
    )

    name = models.CharField(
        max_length=256, 
        help_text='For naming the address like head office or home address.'
    )
    ADDRESS_TYPES = [
        ('Head Office', 'Head Office'),
        ('Billing', 'Billing'),
        ('Shipping', 'Shipping'),
        ('Home', 'Home'),
    ]
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPES, null=True, blank=True)

    address_line_1 = models.CharField(max_length=256)
    address_line_2 = models.CharField(max_length=256, null=True, blank=True)
    address_line_3 = models.CharField(max_length=256, null=True, blank=True)
    
    city = models.CharField(max_length=256, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)

    country = models.ForeignKey(
        'core.Country',
        on_delete=models.PROTECT,
        related_name='address_country',
    )
    state = models.ForeignKey(
        'core.State',
        on_delete=models.PROTECT,
        related_name='address_state'
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['-created_at']
        indexes = [
        models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.latitude} - {self.longitude}"


class Attendance(CustomModel):
    """model for user and trainer attendnce."""

    attendance_id = models.CharField(max_length=256, unique=True)
    ATTENDENCE_OPTIONS = [
        ('Trainer', 'Trainer'),
        ('Member', 'Member')
    ]
    attendence_for = models.CharField(max_length=50, choices=ATTENDENCE_OPTIONS)
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
    bio = models.TextField()
    gallery = models.ForeignKey(
        'user.Gallery',
        on_delete=models.PROTECT,
        related_name="user_profile_gallery",
        null=True, blank=True
    )
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
    CATEGORY = [
        ('PT', 'Personal Trainer'),
        ('All', 'All Rounder'),
        ('AT', 'Athletic Trainer'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY)
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
    
    
