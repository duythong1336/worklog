from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Salary
from .serializers import SalarySerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from Employee.permissions import IsAdminOrStaff
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date, export_salary_excel, update_google_sheet_salary
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.utils import timezone
from openpyxl import Workbook
from django.http import HttpResponse
import os
from django.conf import settings
import threading


class SalaryListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['month','year']
    search_fields = ['employee__username', 'employee__last_name','employee__first_name']
    
    def get(self, request, *args, **kwargs):
        salaries = Salary.objects.all()

        queryset = self.filter_queryset(salaries)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = SalarySerializer(page, many=True)
        
        response = create_paginated_response(serializer, salaries, paginator)
        return Response(response, status=response.get('statusCode'))
    
class SalaryCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAdminOrStaff]
    
    def post(self, request, *args, **kwargs):
        serializer = SalarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = format_respone(success=True, status=status.HTTP_201_CREATED, message="Salaries created successfully", data=None)
            return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response, status=response.get('status'))
        
        

class SalaryGoogleSheetView(generics.CreateAPIView):
    
    permission_classes = [IsAdminOrStaff]
    
    def post(self, request, *args, **kwargs):
        
        month = request.data.get('month')
        year = request.data.get('year')
        employee = request.data.get('employee')
        

        # Lọc dữ liệu dựa trên tháng và năm
        salaries = Salary.objects.all()
        if month and year and employee:
            salaries = salaries.filter(month=month, year=year, employee=employee)
        elif month:
            salaries = salaries.filter(month=month)
        elif year:
            salaries = salaries.filter(year=year)
        elif employee:
            salaries = salaries.filter(employee=employee)

        if not salaries.exists():
            response_data = {
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': "No data found.",
                'data': {}
            }
            return Response(response_data, status=response_data.get('status'))

        # Serialize dữ liệu
        serializer = SalarySerializer(salaries, many=True)

        # Gọi hàm trong serializer để export Excel
        google_sheet_url = update_google_sheet_salary(serializer.data)
        
        # Tạo response
        response_data = {
            'success': True,
            'status': status.HTTP_200_OK,
            'message': "Export Google Sheet successfully",
            'data': {
            'google_sheet_url': google_sheet_url  # Thêm link vào data
        }
        }
        return Response(response_data, status=response_data.get('status'))
        
class SalaryDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        salary_id = kwargs.get('pk')
        try:
            salary = Salary.objects.get(pk=salary_id)
        except Salary.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Salary not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        salary.delete()
        
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Salary deleted successfully", data=[])
        return Response(response_data, status=response_data.get('status'))
    
class SalaryDeleteAllView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        try:
            salary = Salary.objects.all()
        except Salary.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Salary not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        salary.delete()
        
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Salary deleted successfully", data=[])
        return Response(response_data, status=response_data.get('status'))
    
class SalaryProfileView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['month','year']
    # filterset_class = SalaryFilter
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            salary = Salary.objects.filter(employee = user)
            if salary:
                queryset = self.filter_queryset(salary)
        
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(queryset, request)
                serializer = SalarySerializer(page, many=True)
                response = create_paginated_response(serializer, salary, paginator)
                # response = format_respone(success=True, status=status.HTTP_200_OK, message="Get Timekeeping User Successfully", data=serializer.data)
                return Response(response, status=response.get('status'))    
            else:
                response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="salary not found in database", data=[])
                return Response(response, status=response.get('status'))
                
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
        
class ExportSalaryExcel(APIView):
    permission_classes = [IsAdminOrStaff]
    def post(self, request):
        # Lấy các tham số bộ lọc từ request
        month = request.data.get('month')
        year = request.data.get('year')
        employee = request.data.get('employee')

        # Lọc dữ liệu dựa trên tháng và năm
        salaries = Salary.objects.all()
        if month and year and employee:
            salaries = salaries.filter(month=month, year=year, employee=employee)
        elif month:
            salaries = salaries.filter(month=month)
        elif year:
            salaries = salaries.filter(year=year)
        elif employee:
            salaries = salaries.filter(employee=employee)

        if not salaries.exists():
            response_data = {
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': "No data found.",
                'data': []
            }
            return Response(response_data, status=response_data.get('status'))

        # Serialize dữ liệu
        serializer = SalarySerializer(salaries, many=True)

        # Gọi hàm trong serializer để export Excel
        excel_file_path = export_salary_excel(serializer.data)
        
        # Tạo response
        response_data = {
            'success': True,
            'status': status.HTTP_200_OK,
            'message': "Export excel successfully",
            'data': {
                'excel_file_path': excel_file_path
            }
        }
        return Response(response_data, status=response_data.get('status'))