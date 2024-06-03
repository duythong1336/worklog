from django.contrib import admin
from .models import Notification, DeviceToken

admin.site.register(Notification)
admin.site.register(DeviceToken)