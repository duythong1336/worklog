from rest_framework import serializers
from Employee.models import Employee
from .models import StatusChoicesEnum, LeaveRequest
from django.core.mail import send_mail
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class LeaveRequestSerializer(serializers.Serializer):
    
    # employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    reason = serializers.CharField(max_length = 255)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    # status = serializers.ChoiceField(choices=StatusChoicesEnum, default=StatusChoicesEnum.PENDING)
    # created_at = serializers.DateTimeField()
    
    def create(self, validated_data):
        user = self.context['request'].user
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        
        # Kiểm tra xem có yêu cầu nghỉ phép nào khác trong khoảng thời gian đã cho không
        existing_leave_requests = LeaveRequest.objects.filter(
            employee=user,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        
        if existing_leave_requests.exists():
            # Nếu có yêu cầu nghỉ phép khác trong khoảng thời gian đã cho, ném một ngoại lệ hoặc trả về thông báo lỗi
            raise ValidationError("There is already a leave request within the specified date range.")
        
        # Nếu không có yêu cầu nghỉ phép khác trong khoảng thời gian đã cho, tiến hành tạo yêu cầu nghỉ phép mới
        leave_request = LeaveRequest(    
            employee=user,
            reason=validated_data.get('reason'),
            start_date=start_date,
            end_date=end_date,
            created_at=datetime.now()
        )
        
        leave_request.save()
        
        return leave_request

    
    def delete(self, instance):
        instance.delete()
    
    def to_representation(self, instance):
        
        representation = {
            'leave_request_id': instance.id,
            'employee': instance.employee.first_name + " " + instance.employee.last_name,
            'department': instance.employee.department.name,
            'reason': instance.reason,
            'start_date': instance.start_date,
            'end_date': instance.end_date,
            'status': instance.status,
            'created_at': instance.created_at,
        }
        return representation