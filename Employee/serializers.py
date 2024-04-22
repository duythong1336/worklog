from rest_framework import serializers
from .models import Employee, GenderChoices
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

# Lấy tất cả các người dùng admin
admin_users = Employee.objects.filter(is_admin=True)

# Lặp qua từng người dùng admin và gán cho họ các quyền của admin
for admin_user in admin_users:
    admin_permissions = admin_user.user_permissions.all()
    admin_user.user_permissions.set(admin_permissions)

class EmployeeSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 30, validators=[UniqueValidator(queryset=Employee.objects.all())])
    password = serializers.CharField(max_length = 30, write_only=True, validators=[validate_password])
    first_name = serializers.CharField(max_length = 10)
    last_name = serializers.CharField(max_length = 10)
    email = serializers.CharField(max_length = 50, validators=[UniqueValidator(queryset=Employee.objects.all())])
    is_admin = serializers.SerializerMethodField()
    gender = serializers.ChoiceField(choices=GenderChoices, default=GenderChoices.MALE)
    phone_number = serializers.IntegerField()   
    address = serializers.CharField(max_length = 255)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    
    
    def get_is_admin(self, obj):
        return obj.is_admin
    
    def create(self, validated_data):
        
        password = make_password(validated_data['password'])
        
        employee = Employee.objects.create(     
            username=validated_data.get('username'),
            password=password,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            is_admin=False,  
            gender=validated_data.get('gender'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
            department=validated_data.get('department')
        )
        
        employee.save()
        
        email_content = f"Username: {validated_data['username']}\nPassword: {validated_data['password']}"
        
        send_mail(
            "[Exnodes] Username and password new Employee",
            email_content,
            "",
            [validated_data.get('email')],
            fail_silently=False,
        )
        
        
        
        return employee
    
    def update(self, instance, validated_data):
        
        # instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.department = validated_data.get('department', instance.department)
        
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
    
    def to_representation(self, instance):
        
        representation = {
            'id': instance.id,
            'username': instance.username,
            # 'password': instance.password,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'is_admin': instance.is_admin,
            'gender': instance.gender,
            'phone_number': instance.phone_number,
            'address': instance.address,
            'department': instance.department.name
        }
        return representation
    
class EmployeeUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 10)
    last_name = serializers.CharField(max_length = 10)
    gender = serializers.ChoiceField(choices=GenderChoices, default=GenderChoices.MALE)
    phone_number = serializers.IntegerField()
    address = serializers.CharField(max_length = 255)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        
        representation = {
            'id': instance.id,
            'username': instance.username,
            # 'password': instance.password,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'is_admin': instance.is_admin,
            'gender': instance.gender,
            'phone_number': instance.phone_number,
            'address': instance.address,
            'department': instance.department.name
        }
        return representation
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")

#         employee = Employee.objects.filter(username=username).first()

#         if employee is None or not employee.check_password(password):
#             raise serializers.ValidationError("Invalid username or password")

#         refresh = RefreshToken.for_user(employee)
        
#         return {
#             'username': employee.username,
#             'email': employee.email,
#             'token': {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#         }
    
        
