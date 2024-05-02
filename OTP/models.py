from django.db import models
from Employee.models import Employee

class OTP(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
