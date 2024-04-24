from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.generics import ListAPIView
from .models import Employee, LeaveRequest
from .serializers import LeaveRequestSerializer
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from Employee.permissions import IsAdminOrStaff
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail


class LeaveRequestCreateView(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
    
            serializer = LeaveRequestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response = format_respone(success=True, status=status.HTTP_201_CREATED, message="LeaveRequest created successfully", data=serializer.data)
                return Response(response, status=response.get('status'))
            else:
                response = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)
                return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
        
class LeaveRequestListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get(self, request, *args, **kwargs):
        leave_requests = LeaveRequest.objects.all()

        queryset = self.filter_queryset(leave_requests)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = LeaveRequestSerializer(page, many=True)
        
        response = create_paginated_response(serializer, leave_requests, paginator)
        return Response(response, status=response.get('statusCode'))
    
class LeaveRequestSearchView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee__username', 'employee__last_name','employee__first_name']
    
    def get(self, request, *args, **kwargs):
        leave_requests = LeaveRequest.objects.all()

        queryset = self.filter_queryset(leave_requests)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = LeaveRequestSerializer(page, many=True)
        
        response = create_paginated_response(serializer, leave_requests, paginator)
        return Response(response, status=response.get('statusCode'))
    
class ApprovedStatusView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrStaff]
    def post(self, request, *args, **kwargs):
        leave_request_id = kwargs.get('pk')
        try:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
        except LeaveRequest.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="LeaveRequest not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        if leave_request.status != "PENDING":
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Status is not PENDING", data=[])
            return Response(response_data, status=response_data.get('status'))

        leave_request.status = "APPROVED"  
        leave_request.save()
        
        last_name = leave_request.employee.last_name
        first_name = leave_request.employee.first_name
        start_date = format_date(leave_request.start_date)
        end_date = format_date(leave_request.end_date)
        
        email_content = f"Xin chào: {first_name} {last_name},\nĐơn xin nghỉ phép của bạn từ ngày {start_date} đến ngày {end_date} đã được xác nhận đồng ý "
        
        send_mail(
            "[Exnodes] Đơn xin nghỉ phép",
            email_content,
            "",
            [leave_request.employee.email],
            fail_silently=False,
        )

        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="LeaveRequest approved", data=[])
        return Response(response_data, status=response_data.get('status'))
    
class RejectedStatusView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminOrStaff]
    def post(self, request, *args, **kwargs):
        leave_request_id = kwargs.get('pk')
        try:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
        except LeaveRequest.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="LeaveRequest not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        if leave_request.status != "PENDING":
            response_data = format_respone(success=False, status=status.HTTP_400_BAD_REQUEST, message="Status is not PENDING", data=[])
            return Response(response_data, status=response_data.get('status'))

        leave_request.status = "REJECTED"
        leave_request.save()

        last_name = leave_request.employee.last_name
        first_name = leave_request.employee.first_name
        start_date = format_date(leave_request.start_date)
        end_date = format_date(leave_request.end_date)
        
        
        email_content = f"Xin chào: {first_name} {last_name},\nĐơn xin nghỉ phép của bạn từ ngày {start_date} đến ngày {end_date} đã đã bị từ chối"
        
        send_mail(
            "[Exnodes] Đơn xin nghỉ phép",
            email_content,
            "",
            [leave_request.employee.email],
            fail_silently=False,
        )

        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="LeaveRequest rejected", data=[])
        return Response(response_data, status=response_data.get('status'))
        
class LeaveRequestDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        leave_request_id = kwargs.get('pk')
        try:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
        except LeaveRequest.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="LeaveRequest not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        leave_request.delete()
        
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="LeaveRequest deleted successfully", data=[])
        return Response(response_data, status=response_data.get('status'))
            