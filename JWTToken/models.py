from django.db import models
# from django.contrib.auth.models import AbstractUser

class JWTToken(models.Model):
    
    token = models.CharField(max_length=500)
    user_id = models.IntegerField()
    username = models.CharField(max_length=30)
    roles = models.CharField(max_length=50)
    issued_at = models.DateTimeField()
    expiration_time = models.DateTimeField()
    issuer = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 100)
    audience = models.CharField(max_length = 100)
    ip_address = models.CharField(max_length = 100)
    user_agent = models.CharField(max_length = 100)
    device_id = models.CharField(max_length = 100)
    is_expired = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.token}"