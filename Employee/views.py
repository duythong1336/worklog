from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeUpdateSerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrStaff
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

class EmployeeListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']
    
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()

        queryset = self.filter_queryset(employees)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = EmployeeSerializer(page, many=True)
        
        response = create_paginated_response(serializer, employees, paginator)
        return Response(response, status=response.get('statusCode'))
    
class EmployeeSearchListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'last_name','first_name']
    
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()

        queryset = self.filter_queryset(employees)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = EmployeeSerializer(page, many=True)
        
        response = create_paginated_response(serializer, employees, paginator)
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
    def put(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        employee = get_object_or_404(Employee, pk=employee_id)
        serializer = EmployeeUpdateSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer = EmployeeSerializer(employee, data=request.data)
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
        
        
    
