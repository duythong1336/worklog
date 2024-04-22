from django.db import models
# from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    
    name = models.CharField(max_length=150)


    def __str__(self):
        return f"{self.name}"