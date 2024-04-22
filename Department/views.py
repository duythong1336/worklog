from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Department
from .serializers import DepartmentSerializer
from share.utils import format_respone
from django.shortcuts import get_object_or_404
from Employee.permissions import IsAdminOrStaff


class DepartmentListView(APIView):
    
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()  
        serializer = DepartmentSerializer(departments, many=True)
        response = format_respone(success=True, status=status.HTTP_200_OK, message="Success", data=serializer.data)
        
        return Response(response, status=response.get('status'))
    
class DepartmentCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminOrStaff]
    def post(self, request, *args, **kwargs):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = format_respone(success=True, status=status.HTTP_201_CREATED, message="Department created successfully", data=serializer.data)
            return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response, status=response.get('status'))
        
class DepartmentUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrStaff]
    def put(self, request, *args, **kwargs):
        department_id = kwargs.get('pk')
        department = get_object_or_404(Department, pk=department_id)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Department updated successfully", data=serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class DepartmentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        department_id = kwargs.get('pk')
        department = get_object_or_404(Department, pk=department_id)
        department.delete()
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Department deleted successfully", data=[])
        return Response(response_data, status=status.HTTP_200_OK)
