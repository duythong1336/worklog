from django.db import models
from Employee.models import Employee

class TypeCheckChoicesEnum(models.TextChoices):
    CHECKIN = 'CHECKIN', 'Checkin'
    CHECKOUT = 'CHECKOUT', 'Checkout'
    RAVAO = 'RAVAO', 'Ra vào'

class Timekeeping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='time_keeping')
    check_type = models.CharField(max_length=10, choices=TypeCheckChoicesEnum.choices, default='CHECKIN')
    date = models.DateField(auto_now_add=True)
    check_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Checkin out for {self.employee.username}"