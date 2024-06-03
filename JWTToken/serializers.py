from rest_framework import serializers
from Employee.models import Employee, GenderChoices
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import JWTToken
from datetime import datetime, timedelta
from Notification.models import DeviceToken
import uuid

def generate_server_device_id():
    # Tạo một UUID duy nhất cho device_id của máy chủ
    return str(uuid.uuid4())

class JWTTokenSerializer(serializers.Serializer):
    class Meta:
        model = JWTToken
        fields = '__all__'
        
    def to_representation(self, instance):
        
        representation = {
            'token_id': instance.id,
            'token': instance.token,
            'user_id': instance.user_id,
            'username': instance.username,
            'roles': instance.roles,
            'issued_at': instance.issued_at,
            'expiration_time': instance.expiration_time,
            'issuer': instance.issuer,
            'subject': instance.subject,
            # 'audience': instance.audience,
            'ip_address': instance.ip_address,
            'user_agent' : instance.user_agent,
            'device_id' : instance.device_id,
            'is_expired': instance.is_expired,
        }
        return representation
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        employee = Employee.objects.filter(username=username).first()

        if employee is None or not employee.check_password(password):
            raise serializers.ValidationError("Invalid username or password")

        # Tạo payload cho token
        token_payload = {
            'user_id': employee.id,
            'username': employee.username,
            'roles': 'admin' if employee.is_admin else 'employee',  # Ví dụ: vai trò admin hoặc người dùng
            'issued_at': datetime.now(),
            'expiration_time': datetime.now() + timedelta(weeks=1),  # Ví dụ: token hết hạn sau 7 ngày
            'subject': 'authentication',
            'issuer': 'localhost',  # Thay thế bằng thông tin phát hành token của bạn
            'audience': '',  # Thay thế bằng đối tượng mà token được phát hành cho
            'ip_address': self.context['request'].META.get('REMOTE_ADDR'),
            'user_agent': self.context['request'].META.get('HTTP_USER_AGENT'),  # Thông tin trình duyệt hoặc ứng dụng sử dụng
            'device_id': generate_server_device_id(),  # Thay thế bằng ID của thiết bị nếu có
            'is_expired': False,
        }

        # Tạo token
        access_token = AccessToken.for_user(employee)
        refresh = RefreshToken.for_user(employee)
        token = str(access_token)

        # Lưu thông tin vào JWTToken
        jwt_token = JWTToken(
            token=token,
            user_id=employee.id,
            username=employee.username,
            roles='admin' if employee.is_admin else 'user',
            issued_at=token_payload['issued_at'],
            expiration_time=token_payload['expiration_time'],
            issuer=token_payload['issuer'],
            subject=token_payload['subject'],
            audience=token_payload['audience'],
            ip_address=token_payload['ip_address'],
            user_agent=token_payload['user_agent'],
            device_id=token_payload['device_id'],
            is_expired=token_payload['is_expired'],
        )
        jwt_token.save()
        
        # register_device_for_user(employee, self.context['request'])

        return {
            'username': employee.username,
            'email': employee.email,
            'token': {
                'refresh': str(refresh),
                'access': token,
            }
        }
        
# def gather_device_info(request):
#     # Lấy thông tin thiết bị từ tiêu đề của yêu cầu
#     # platform = request.headers.get('User-Agent')  # Lấy thông tin về trình duyệt
#     # language = request.headers.get('Accept-Language')  # Lấy thông tin về ngôn ngữ

#     platform = 'WEB'
#     language = 'en'
#     token = 'test'

#     # Tạo dictionary chứa thông tin thiết bị
#     device_info = {
#         'platform': platform,
#         'language': language,
#         'token': token
#     }

#     return device_info

# def register_device_for_user(employee, request):
#     # Thu thập thông tin thiết bị
#     device_info = gather_device_info(request)

#     if device_info:
#         # Lưu thông tin đăng ký thiết bị vào cơ sở dữ liệu
#         save_device_info(employee, device_info)


# def save_device_info(employee, device_info):
#     # Lưu thông tin thiết bị vào cơ sở dữ liệu
#         DeviceToken.objects.create(
#         user=employee,
#         token=device_info['token'],
#         platform=device_info['platform'],   
#         language=device_info['language'],
#         )