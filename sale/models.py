"""
Sale related models.
"""


from django.db import models

from user.models import CustomModel

# Create your models here.



# sale
class Sale(CustomModel):
    """
    Sale
    """

    sale_id = models.CharField(max_length=256, unique=True)
    