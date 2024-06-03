from django.urls import path
from .views import *

urlpatterns = [
    path('DeviceToken/create/', DeviceTokenCreateView.as_view(), name='DeviceToken-create'),
]
