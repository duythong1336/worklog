from django.db import models
from Employee.models import Employee
from django_filters import rest_framework as filters
from datetime import datetime

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    created_at = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=1)