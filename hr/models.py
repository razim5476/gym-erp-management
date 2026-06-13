"""
HR Models.
"""

from django.db import models
from user.models import CustomModel

# Create your models here.


class Employee(CustomModel):
    """
    Docstring for Employee
    """

    employee_id = models.CharField(max_length=100, unique=True)
    employee_name = models.CharField(max_length=100)
    