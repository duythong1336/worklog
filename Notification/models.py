from django.db import models
from Employee.models import Employee
import firebase_admin
from firebase_admin import credentials, messaging

class Notification(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='notifications')
    title = models.JSONField(default=None, null=True)
    message = models.JSONField(default=None, null=True)
    payloadData = models.JSONField(default=None, null=True)
    isRead = models.BooleanField(default=False)

class DevicePlatform(models.TextChoices):
    WEB = 'WEB'
    ANDROID = 'ANDROID'
    IOS = 'IOS'

class DeviceToken(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='deviceTokens')
    token = models.CharField(max_length=256)
    status = models.BooleanField(default=True)
    platform = models.CharField(
        max_length=10, choices=DevicePlatform.choices, default=DevicePlatform.WEB)
    language = models.CharField(max_length=5, default='en')

class Topic(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

class DeviceTopic(models.Model):
    deviceToken = models.ForeignKey(
        DeviceToken, on_delete=models.CASCADE, related_name='deviceTopics')
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='deviceTopics')
    status = models.BooleanField(default=True)

# cred = credentials.Certificate("exnodes-8257f-firebase-adminsdk-w274t-8a132e3953.json")
# firebase_admin.initialize_app(cred)


# def send_notification(device_tokens, title, message):
#     # Tạo thông báo
#     notification = messaging.Notification(title=title, body=message)
    
#     # Lặp qua danh sách các thiết bị và gửi thông điệp cho mỗi thiết bị
#     for device_token in device_tokens:
#         # Tạo thông điệp cho thiết bị hiện tại
#         message_for_device = messaging.Message(
#             notification=notification,
#             token=device_token,
            
#         )
        
#         # Gửi thông điệp cho thiết bị hiện tại
#         response = messaging.send(message_for_device)
#         print("Response:", response)

# def create_notification(user, title, message):

#     notification = Notification.objects.create(
#         user=user,
#         title=title,
#         message=message,
#     )
#     return notification

