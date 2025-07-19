from django.db import models
from user.models import CustomModel

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
