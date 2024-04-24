from rest_framework import serializers
from Employee.models import Employee
from .models import StatusChoicesEnum, LeaveRequest
from django.core.mail import send_mail
from datetime import datetime, timedelta



class LeaveRequestSerializer(serializers.Serializer):
    
    # employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    reason = serializers.CharField(max_length = 255)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    # status = serializers.ChoiceField(choices=StatusChoicesEnum, default=StatusChoicesEnum.PENDING)
    # created_at = serializers.DateTimeField()
    
    def create(self, validated_data):
        
        user = self.context['request'].user
        leave_request = LeaveRequest(    
            employee = user,
            reason=validated_data.get('reason'),
            start_date=validated_data.get('start_date'),
            end_date=validated_data.get('end_date'),
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