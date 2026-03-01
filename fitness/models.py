from django.db import models
from django.forms import ValidationError
from django_ckeditor_5.fields import CKEditor5Field
from user.models import CustomModel
from core.formatchecker import ContentTypeRestrictedFileField
# Create your models here.


# worrkout
class WorkoutsPlan(CustomModel):
    """Workouts"""

    workout_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=50, unique=True)
    TYPE = [
        ('Fat loss', 'Fat loss'),
        ('Weight Gain', 'Weight Gain'),
        ('Cutting', 'Cutting'),
        ('Bulk', 'Bulk'),
        ('Athletic', 'Athletic')
    ]
    excersises = models.ManyToManyField(
        'fitness.Workouts',
        related_name="workouts_plan"
    )
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = models.CharField(max_length=50, choices=GENDER)
    DIFFICULTY_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='Beginner')

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='workout_plan_branch'
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='workout_plan_company'
    )


    class Meta:
        verbose_name = "Workouts Plan"
        verbose_name_plural = "Workout Plans"
        ordering = ['created_at']


class Workouts(CustomModel):
    """Different parts workouts"""

    workout_id = models.CharField(unique=True, max_length=256)
    BODY_PART = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Leg', 'Leg'),
        ('Shoulder', 'Shoulder'),
        ('Triceps', 'Triceps'),
        ('Glutes', 'Glutes'),
        ('Biceps', 'Biceps'),
        ('Calf', 'Calf')
    ]
    body_part = models.CharField(max_length=50, choices=BODY_PART)
    name = models.CharField(max_length=50)
    description = CKEditor5Field('Description', config_name="extends")
    image = models.URLField(null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    reps = models.IntegerField(default=15)
    sets = models.IntegerField(default=3)

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='workouts_branch'
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='workouts_company'
    )


    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
        ordering = ['-created_at']


# playlist
class Playlist(CustomModel):
    """Different playlist links or files."""

    playlist_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    platform = models.CharField(max_length=50, null=True, blank=True, help_text="Spofity, Youtube, etc.")
    decsription = CKEditor5Field('Playlist', config_name="extends")

    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='playlist_branch'
    )
    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='playlist_company'
    )


    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# multiple songs for playlist:
class PlaylistSongs(CustomModel):
    """Multiple songs for playlist."""

    playlist = models.ForeignKey(
        'fitness.Playlist',
        on_delete=models.PROTECT,
        related_name="playlist_songs"
    )
    songs = ContentTypeRestrictedFileField(upload_to='songs/', content_types=['audio/mpeg', 'audio/mp3'], max_upload_size=20971520, blank=True, null=True)
    title = models.CharField(max_length=256)
    playlist_url = models.URLField(null=True, blank=True)

    def clean(self):
        """validation for one field must be filled either songs or playlist url."""
        if not self.songs and not self.playlist_url:
            raise ValidationError("Must fill either songs field or the playlist url field.")

    class Meta:
        verbose_name = "Playlist Song"
        verbose_name_plural = "Playlist Songs"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.playlist.name}"


# diet model:
class Diet(CustomModel):
    """Diets"""

    diet_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    descritpion = CKEditor5Field('Diet', config_name='extends')
    TYPE = [
        ('Keto', 'Keto'),
        ('Vegetarian', 'Vegetarian'),
        ('Non-Veg', 'Non-Veg')
    ]
    diet_type = models.CharField(max_length=20, choices=TYPE)
    GOAL_TYPE = [
        ('Weight Loss', 'Weight Loss'),
        ('Weight Gain', 'Weight Gain')
    ]
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE)
    duration = models.CharField(max_length=50, null=True, blank=True)
    calorie_range = models.IntegerField(null=True, blank=True)

    company = models.ForeignKey(
        'organization.Company',
        on_delete=models.PROTECT,
        related_name='diet_plan_company'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.PROTECT,
        related_name='diet_branch'
    )


    class Meta:
        verbose_name = "Diet"
        verbose_name_plural = "Diets"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# detailed diet foe the day:
class DietDetail(CustomModel):
    """Diet for the day with breakfast, luch etc."""

    diet_day = models.CharField(max_length=256, help_text='like day1, day2, etc')
    diet = models.ForeignKey(
        'fitness.Diet',
        on_delete=models.PROTECT,
        related_name="diet_diet_details"
    )
    CHOICE = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Before Workout', 'Before Workout'),
        ('After Workout', 'After Workout'),
        ('Supper', 'Supper')
    ]
    part_of_day = models.CharField(max_length=20, choices=CHOICE)
    food_items = models.ManyToManyField(
        'fitness.Item',
        related_name="food_items"
    )

    class Meta:
        unique_together = ('diet', 'diet_day', 'part_of_day')
        ordering = ['created_at']
        verbose_name = "Diet Detail"
        verbose_name_plural = "Diet Details"

    def __str__(self):
        return f"{self.diet.name} - {self.diet_day} - {self.part_of_day}"


# fod items and therit details:
class Item(CustomModel):
    """food item and their details."""

    item_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)

    category = models.ForeignKey(
        'fitness.ItemCategory',
        on_delete=models.PROTECT,
        related_name="item_categorys"
    )
    uom = models.ForeignKey(
        'core.UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name="item_uom"
    )

    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"

    def __str__(self):
        return self.name


# item categories:
class ItemCategory(CustomModel):
    """Item categories for food items."""

    item_category_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Item Category"
        verbose_name_plural = "Item Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# item macros details:
class ItemMacros(CustomModel):
    """macros like protein , carbs and etc details."""

    item_macros_id = models.CharField(max_length=256, unique=True)
    item = models.ForeignKey(
        'fitness.Item',
        on_delete=models.PROTECT,
        related_name='item_macros'
    )
    protein = models.PositiveIntegerField(default=0)
    fat = models.PositiveIntegerField(default=0)
    carbs = models.PositiveIntegerField(default=0)
    calories = models.PositiveIntegerField(default=0)
    sugar = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Item Macros"
        verbose_name_plural = "Item Macros"
        ordering = ['-created_at']

    def __str__(self):
        return self.item.name



