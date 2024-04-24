from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.generics import ListAPIView
from .models import Employee, Timekeeping, TypeCheckChoicesEnum
from .serializers import TimekeepingSerializer
from share.utils import format_respone, LargeResultsSetPagination, get_paginated_response, create_paginated_response, format_date, update_excel_file
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from Employee.permissions import IsAdminOrStaff
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from datetime import date


class CheckinCheckoutView(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        today = date.today()
        user = request.user
        serializer = TimekeepingSerializer(data=request.data, context={'request': request})
        if user.is_authenticated:
            checkin_records = Timekeeping.objects.filter(employee=user, check_type=TypeCheckChoicesEnum.CHECKIN, date=today)
            checkout_records = Timekeeping.objects.filter(employee=user, check_type=TypeCheckChoicesEnum.CHECKOUT, date=today)
            if not checkin_records.exists():
                serializer.is_valid()
                serializer.save()
                update_excel_file(user, TypeCheckChoicesEnum.CHECKIN)
                response = format_respone(success=True, status=status.HTTP_201_CREATED, message="Checkin successfully", data=[])
                return Response(response, status=response.get('status'))
            elif checkin_records.exists() and not checkout_records.exists():
                serializer.is_valid()
                serializer.save()
                update_excel_file(user, TypeCheckChoicesEnum.CHECKOUT)
                response = format_respone(success=True, status=status.HTTP_201_CREATED, message="Checkout successfully", data=[])
                return Response(response, status=response.get('status'))
            else:
                serializer.is_valid()
                serializer.save()
                update_excel_file(user, TypeCheckChoicesEnum.RAVAO)
                response = format_respone(success=True, status=status.HTTP_201_CREATED, message="RAVAO successfully", data=[])
                return Response(response, status=response.get('status'))
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
        
class CheckinCheckoutListView(ListAPIView):
    
    permission_classes = [IsAdminOrStaff]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date','employee__id']
    
    def get(self, request, *args, **kwargs):
        time_keeping = Timekeeping.objects.all()

        queryset = self.filter_queryset(time_keeping)
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        serializer = TimekeepingSerializer(page, many=True)
        
        response = create_paginated_response(serializer, time_keeping, paginator)
        return Response(response, status=response.get('statusCode'))
    
class TimeKeepingDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminOrStaff]
    def delete(self, request, *args, **kwargs):
        time_keeping_id = kwargs.get('pk')
        try:
            time_keeping = Timekeeping.objects.get(pk=time_keeping_id)
        except Timekeeping.DoesNotExist:
            response_data = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Timekeeping not found in database", data=[])
            return Response(response_data, status=response_data.get('status'))
        
        time_keeping.delete()
        
        response_data = format_respone(success=True, status=status.HTTP_200_OK, message="Timekeeping deleted successfully", data=[])
        return Response(response_data, status=response_data.get('status'))
    
class TimekeepingsOneUserView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_authenticated:
            time_keeping = Timekeeping.objects.filter(employee = user)
            if time_keeping:
                serializer = TimekeepingSerializer(time_keeping, many=True)
                response = format_respone(success=True, status=status.HTTP_200_OK, message="Get Timekeeping User Successfully", data=serializer.data)
                return Response(response, status=response.get('status'))    
            else:
                response = format_respone(success=False, status=status.HTTP_404_NOT_FOUND, message="Timekeeping Employee not found in database", data=[])
                return Response(response, status=response.get('status'))
                
        else:
            response = format_respone(success=False, status=status.HTTP_401_UNAUTHORIZED, message="User is not authenticated", data=[])
            return Response(response, status=response.get('status'))
            