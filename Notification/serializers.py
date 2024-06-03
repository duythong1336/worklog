from rest_framework import serializers
from .models import DeviceToken
from OTP.models import OTP
from Department.models import Department
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from jwt import encode as jwt_encode
from JWTToken.models import JWTToken
from datetime import datetime, timedelta
from WorkLog.settings import SECRET_KEY
from random import randint
from django.utils import timezone


class DeviceTokenSerializer(serializers.Serializer):
    
    token = serializers.CharField()
    platform = serializers.CharField()
    language = serializers.CharField()


    def create(self, validated_data):
        user = self.context['request'].user
        
        device_token = DeviceToken(     
            user = user,
            token=validated_data.get('token'),
            platform=validated_data.get('platform'),
            language=validated_data.get('language'),
        )
        
        device_token.save()
        
        return device_token
    
    def to_representation(self, instance):
        
        representation = {
            'device_token_id': instance.id,
            'user': instance.user.username,
            'token': instance.token,
            'status': instance.status,
            'platform': instance.platform,
            'language': instance.language,
        }
        return representation