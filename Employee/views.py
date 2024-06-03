from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeUpdateSerializer, ChangePasswordRequestSerializer, NewPasswordSerializer, EmployeeUpdateAdminSerializer, upload_file, ForgotPassSerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrStaff
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from OTP.models import OTP
from django.utils import timezone
from rest_framework.parsers import MultiPartParser
from datetime import timedelta
from django.utils import timezone

class EmployeeListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['username', 'last_name','first_name']
    
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()

        queryset = self.filter_queryset(employees)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = EmployeeSerializer(page, many=True)
        
        response = create_paginated_response(serializer, employees, paginator)
        return Response(response, status=response.get('statusCode'))
    
class EmployeeGetOneView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request, *args, **kwargs):
        
        pk = kwargs.get('pk')
        
        employee = Employee.objects.get(id=pk)
        
        serializer = EmployeeSerializer(employee)
        
        response = format_respone(success=True, status=status.HTTP_200_OK, message="Employee get successfully", data=serializer.data)
        return Response(response, status=response.get('statusCode'))
    
class EmployeeCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAdminOrStaff]
    
    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():   
            serializer.save()
            
            response = format_respone(success=True, status=status.HTTP_201_CREATED, message="Employee created successfully", data=serializer.data)
            return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response, status=response.get('status'))
        
class EmployeeUpdateView(generics.RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser]
    def put(self, request, *args, **kwargs):
        
        user = request.user
        employee = Employee.objects.get(id=user.id)
        serializer = EmployeeUpdateSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            upload_file(request)
            response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Employee updated successfully", data=serializer.data)
            return Response(response_data, status=response_data.get('status'))
        else:
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response_data, status=response_data.get('status'))

class EmployeeUpdateAdminView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrStaff]
    def put(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeUpdateAdminSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Employee updated successfully", data=serializer.data)
            return Response(response_data, status=response_data.get('status'))
        else:
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response_data, status=response_data.get('status'))
        
class EmployeeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        empolyee = get_object_or_404(Employee, pk=employee_id)
        empolyee.delete()
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Empolyee deleted successfully", data=[])
        return Response(response_data, status=response_data.get('status'))
    
class EmployeeProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_authenticated:
            employee = Employee.objects.get(id = user.id)
            if employee:
                serializer = EmployeeSerializer(employee)
                response = format_respone(success=True, status=status.HTTP_200_OK, message="Get Employee Profile Successfully", data=serializer.data)
                return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Employee not found in database", data=[])
                return Response(response, status=response.get('status'))
                
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
        
class ChangePasswordRequestAPIView(APIView):
    def post(self, request):    
        user = request.user
        if user.is_authenticated:
            serializer = ChangePasswordRequestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                current_password = serializer.validated_data.get('current_password') 
                if not user.check_password(current_password):
                    response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Mật khẩu hiện tại không đúng.", data=[])
                    return Response(response, status=response.get('status'))
                serializer.save()
                response = format_respone(success=True, status=status.HTTP_200_OK, message="OTP Send to mail successfully", data=[])
                return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message=serializer.errors, data=[])
                return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))

class NewPasswordAPIView(APIView):
    def put(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = NewPasswordSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():

                new_password = serializer.validated_data.get('new_password')
                confirm_new_password = serializer.validated_data.get('confirm_new_password')
                otp_code = serializer.validated_data.get('otp')

                otp_record = OTP.objects.filter(employee=user, otp_code=otp_code).first()
                if not otp_record:
                    response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Mã OTP không hợp lệ.", data=[])
                    return Response(response, status=response.get('status'))

                if otp_record.created_at + timezone.timedelta(minutes=1) < timezone.now():
                    response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Mã OTP đã hết hạn.", data=[])
                    return Response(response, status=response.get('status'))
            
                if new_password != confirm_new_password:
                    response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Mật khẩu mới và mật khẩu xác nhận không khớp.", data=[])
                    return Response(response, status=response.get('status'))

                serializer.save()
                OTP.objects.filter(employee=user).delete()
            
                response = format_respone(success=True, status=status.HTTP_200_OK, message="Thay đổi mật khẩu thành công.", data=[])
                return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message=serializer.errors, data=[])
                return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
        
class ForgotPassView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ForgotPassSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                response = format_respone(success=True, status=status.HTTP_200_OK, message="OTP Send to mail successfully", data=[])
                return Response(response, status=response.get('status'))
            except Exception as e:
                response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message=str(e), data=[])
                return Response(response, status=response.get('status'))
        response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message=serializer.errors, data=[])
        return Response(response, status=response.get('status'))
    
    def patch(self, request):
        # Lấy thông tin từ yêu cầu
        otp_code = request.data.get('otp_code', None)
        new_password = request.data.get('new_password', None)
        confirm_password = request.data.get('confirm_password', None)
    
        # Kiểm tra xem mã OTP và mật khẩu mới có tồn tại trong yêu cầu không
        if not otp_code or not new_password or not confirm_password:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="OTP code, new password, and confirm password are required", data=[])
            return Response(response, status=response.get('status'))
        
        # Kiểm tra mật khẩu mới và mật khẩu xác nhận có khớp nhau không
        if new_password != confirm_password:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="New password and confirm password do not match", data=[])
            return Response(response, status=response.get('status'))

        try:
            # Xác thực mã OTP
            otp_obj = OTP.objects.get(otp_code=otp_code)
            
            expiration_time = otp_obj.created_at + timedelta(minutes=1)
            if timezone.now() > expiration_time:
                response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="OTP code has expired", data=[])
                return Response(response, status=response.get('status'))
        
            # Lấy người dùng tương ứng với mã OTP
            user = otp_obj.employee
        
            # Thiết lập mật khẩu mới cho người dùng
            user.set_password(new_password)
            user.save()
        
            # Xóa mã OTP đã sử dụng
            otp_obj.delete()
        
            # Trả về phản hồi thành công
            response = format_respone(success=True, status=status.HTTP_200_OK, message="Password updated successfully", data=[])
            return Response(response, status=response.get('status'))
        except OTP.DoesNotExist:
            # Nếu không tìm thấy mã OTP
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid OTP code", data=[])
            return Response(response, status=response.get('status'))
        except Exception as e:
            # Xử lý lỗi nếu có
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message=str(e), data=[])
            return Response(response, status=response.get('status'))