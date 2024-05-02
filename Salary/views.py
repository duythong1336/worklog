from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Salary
from .serializers import SalarySerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from Employee.permissions import IsAdminOrStaff
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.utils import timezone

class SalaryListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee','month','year']
    
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
            