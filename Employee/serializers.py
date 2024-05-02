from rest_framework import serializers
from .models import Employee, GenderChoices
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
    salary = serializers.DecimalField(max_digits=11, decimal_places=2)
    
    
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
            department=validated_data.get('department'),
            salary=validated_data.get('salary'),
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
        instance.salary = validated_data.get('salary', instance.salary)
        
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
            'department': instance.department.name,
            'salary': instance.salary,
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
            'department': instance.department.name,
            'salary': instance.salary,
        }
        return representation

class EmployeeUpdateAdminSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 10)
    last_name = serializers.CharField(max_length = 10)
    gender = serializers.ChoiceField(choices=GenderChoices, default=GenderChoices.MALE)
    phone_number = serializers.IntegerField()
    address = serializers.CharField(max_length = 255)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    salary = serializers.DecimalField(max_digits=11, decimal_places=2)
    
    def update(self, instance, validated_data):
        
        # instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.department = validated_data.get('department', instance.department)
        instance.salary = validated_data.get('salary', instance.salary)
        
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
            'department': instance.department.name,
            'salary': instance.salary,
        }
        return representation
        
class ChangePasswordRequestSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=30)

    def save(self, **kwargs):
        # Kiểm tra mật khẩu hiện tại của người dùng
        user = self.context['request'].user


        # Tạo và lưu mã OTP vào cơ sở dữ liệu
        otp = ''.join([str(randint(0, 9)) for _ in range(6)])
        OTP.objects.create(employee=user, otp_code=otp)

        # Gửi mã OTP qua email
        send_mail(
            "[Exnodes] Mã OTP để xác nhận đổi mật khẩu",
            f"Mã OTP của bạn là: {otp}",
            "",
            [user.email],
            fail_silently=False,
        )

        return {"message": "Mã OTP đã được gửi qua email của bạn."}
    
# class VerifyOTPSerializer(serializers.Serializer):
#     otp = serializers.CharField(max_length=6)

#     def validate(self, data):
#         otp_entered = data.get('otp')
#         user = self.context['user']

#         # Kiểm tra mã OTP trong cơ sở dữ liệu
#         otp_record = OTP.objects.filter(employee=user, otp_code=otp_entered, is_used=False).first()

#         if not otp_record:
#             raise serializers.ValidationError("Mã OTP không hợp lệ")
        
#         current_time_naive = timezone.localtime(timezone.now())

#         # Kiểm tra thời gian hiện tại so với thời gian tạo OTP
#         if otp_record.created_at + timedelta(minutes=1) < current_time_naive:
#             raise serializers.ValidationError("Mã OTP đã hết hạn.")

#         data['otp'] = otp_record  # Lưu đối tượng OTP vào validated data
#         return data
    
# class NewPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(max_length=30)
#     confirm_new_password = serializers.CharField(max_length=30)
    

#     def validate(self, data):
#         new_password = data.get('new_password')
#         confirm_new_password = data.get('confirm_new_password')
#         # user = self.context['user']

#         # Kiểm tra xem mật khẩu mới và mật khẩu xác nhận có khớp nhau không
#         if new_password != confirm_new_password:
#             raise serializers.ValidationError("Mật khẩu mới và mật khẩu xác nhận không khớp.")

#         return data

class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=30)
    confirm_new_password = serializers.CharField(max_length=30)
    otp = serializers.CharField(max_length=6)
    
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']

        # Cập nhật mật khẩu mới cho người dùng
        user.set_password(new_password)
        user.save()

    # def validate(self, data):
    #     new_password = data.get('new_password')
    #     confirm_new_password = data.get('confirm_new_password')

    #     # Kiểm tra xem mật khẩu mới và mật khẩu xác nhận có khớp nhau không
    #     if new_password != confirm_new_password:
    #         raise serializers.ValidationError("Mật khẩu mới và mật khẩu xác nhận không khớp.")

        
    #     return data