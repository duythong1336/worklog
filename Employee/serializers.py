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
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import threading
import random
import string
import time

class EmployeeSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 30, validators=[UniqueValidator(queryset=Employee.objects.all())])
    password = serializers.CharField(max_length = 30, write_only=True, validators=[validate_password])
    first_name = serializers.CharField(max_length = 10)
    last_name = serializers.CharField(max_length = 10)
    email = serializers.EmailField(max_length = 50, validators=[UniqueValidator(queryset=Employee.objects.all())])
    is_admin = serializers.SerializerMethodField()
    gender = serializers.ChoiceField(choices=GenderChoices, default=GenderChoices.MALE)
    # phone_number = serializers.IntegerField()   
    # address = serializers.CharField(max_length = 255)
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
            # phone_number=validated_data.get('phone_number'),
            # address=validated_data.get('address'),
            department=validated_data.get('department'),
            salary=validated_data.get('salary'),
        )
        
        employee.save()
        
        email_content = f"Username: {validated_data['username']}\nPassword: {validated_data['password']}"
    
        # Bắt đầu một luồng mới để gửi email
        email_thread = threading.Thread(
        target=send_email_async,
        args=(
            "[Exnodes] Username and password new Employee",
            email_content,
            validated_data.get('email')
        )
        )
        email_thread.start()
        # email_thread.join()
        
        
        
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
            'image': instance.image.name if instance.image else None  # Kiểm tra nếu có hình ảnh trước khi truy cập
        }
        return representation
def send_email_async(email_subject, email_content, recipient_email):
    send_mail(
        email_subject,
        email_content,
        "",
        [recipient_email],
        fail_silently=False,
    )
    
class EmployeeUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 10)
    last_name = serializers.CharField(max_length = 10)
    email = serializers.EmailField(max_length = 50, validators=[UniqueValidator(queryset=Employee.objects.all())])
    gender = serializers.ChoiceField(choices=GenderChoices, default=GenderChoices.MALE)
    phone_number = serializers.IntegerField()
    address = serializers.CharField(max_length = 255)
    image = serializers.ImageField()
    
    # def validate_email(self, value):
    #     # Kiểm tra xem địa chỉ email đã tồn tại trong hệ thống chưa
    #     if Employee.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email address is already in use.")
    #     return value

    # def validate_gender(self, value):
    #     # Kiểm tra xem giá trị của gender có nằm trong danh sách các lựa chọn không
    #     if value not in dict(GenderChoices).keys():
    #         raise serializers.ValidationError("Invalid gender.")
    #     return value

    
    def update(self, instance, validated_data):
        
        # Xác minh và xử lý hình ảnh mới nếu có
        image = validated_data.pop('image', None)
        if image:
            instance.image = image.name
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.email = validated_data.get('email', instance.email)
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
            'image': instance.image.name if instance.image else None  # Kiểm tra nếu có hình ảnh trước khi truy cập
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
    email = serializers.EmailField(max_length = 50, validators=[UniqueValidator(queryset=Employee.objects.all())])
    
    def update(self, instance, validated_data):
        
        # instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
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
            'image': instance.image.name if instance.image else None  # Kiểm tra nếu có hình ảnh trước khi truy cập
        }
        return representation
        
class ChangePasswordRequestSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=30)

    def save(self, **kwargs):
        # Kiểm tra mật khẩu hiện tại của người dùng
        user = self.context['request'].user


        # Tạo và lưu mã OTP vào cơ sở dữ liệu
        otp = generate_unique_otp()
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
    
generated_otps = set()

def generate_unique_otp():
    while True:
        # Tạo một chuỗi ngẫu nhiên gồm 6 chữ số
        otp = ''.join(random.choices(string.digits, k=6))

        # Kiểm tra xem mã OTP đã tồn tại trong danh sách chưa
        if otp not in generated_otps:
            # Nếu không trùng lặp, thêm mã OTP vào danh sách và trả về
            generated_otps.add(otp)
            return otp

    
class ForgotPassSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField(required=False)
    
    def save(self, **kwargs):
        # Kiểm tra mật khẩu hiện tại của người dùng
        user = None
        if 'username' in self.validated_data:
            username = self.validated_data.get('username')
            user = Employee.objects.filter(username=username).first()
        elif 'email' in self.validated_data:
            email = self.validated_data.get('email')
            user = Employee.objects.filter(email=email).first()
        
        if user:
            # Tạo và lưu mã OTP vào cơ sở dữ liệu
            otp = generate_unique_otp()
            # print(otp)
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
        else:
            raise serializers.ValidationError("Không tìm thấy người dùng với thông tin được cung cấp.")
    
def save_uploaded_file(file, folder_path):
    """
    Hàm này nhận một tệp đã được tải lên và một đường dẫn đến thư mục, sau đó lưu tệp vào thư mục đã chỉ định.
    :param file: Tệp đã được tải lên.
    :param folder_path: Đường dẫn đến thư mục để lưu trữ tệp.
    :return: Đường dẫn tuyệt đối đến tệp sau khi lưu.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    fs = FileSystemStorage(location=folder_path)
    filename = fs.save(file.name, file)
    return fs.path(filename)

def upload_file(request):
    if request.method == 'PUT' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        folder_path = os.path.join(settings.MEDIA_ROOT, 'images', 'employee')
        
        # Kiểm tra xem tệp đã tải lên là một tệp ảnh hợp lệ
        if isinstance(uploaded_file, InMemoryUploadedFile) and uploaded_file.content_type.startswith('image'):
            # saved_path = save_uploaded_file(uploaded_file, folder_path)
            thread = threading.Thread(target=save_uploaded_file, args=(uploaded_file, folder_path))
            thread.start()
            thread.join()

            # Đợi cho đến khi luồng hoàn thành trước khi tiếp tục
            return "Image upload started in background thread."
        else:
            return "Invalid file type or no file uploaded."
    else:
        return "No file uploaded."