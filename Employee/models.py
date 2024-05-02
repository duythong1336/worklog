from django.db import models
from django.contrib.auth.models import AbstractUser
from Department.models import Department
from django.contrib.auth.models import User, Permission


class GenderChoices(models.TextChoices):
    MALE = 'Male', 'Nam'
    FEMALE = 'Female', 'Nữ'

class Employee(AbstractUser):
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=7, choices=GenderChoices.choices)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    salary = models.DecimalField(max_digits=11, decimal_places=2, default = 0.0)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
        # Add related_name for reverse accessor
    class Meta:
        permissions = (
            ('employee_groups', 'Employee groups'),
        )
        
    def get_is_admin(self, obj):
    # Kiểm tra xem obj có phải là admin hay không
        return obj.is_admin
    
    # Add related_name to resolve clashes with auth.User.groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_groups',  # You can change 'employee_groups' to whatever name you prefer
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    # Add related_name to resolve clashes with auth.User.user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_user_permissions',  # You can change 'employee_user_permissions' to whatever name you prefer
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    

