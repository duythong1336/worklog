from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeUpdateSerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrStaff

class EmployeeListView(APIView):
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()  
        serializer = EmployeeSerializer(employees, many=True)
        response = format_respone(success=True, status=status.HTTP_200_OK, message="Get Employee Success", data=serializer.data)
        
        return Response(response, status=response.get('status'))
    
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
    
