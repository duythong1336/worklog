from rest_framework import serializers
from Employee.models import Employee
from .models import Timekeeping, TypeCheckChoicesEnum
from datetime import datetime, timedelta
from datetime import date


class TimekeepingSerializer(serializers.Serializer):
     
    
    def create(self, validated_data):
        user = self.context['request'].user
        today = date.today()
        
        # Đếm số lượng bản ghi cho ngày hiện tại và người dùng hiện tại
        time_keeping_user_count = Timekeeping.objects.filter(
            employee=user,
            date=today
        ).count()
        
        print(time_keeping_user_count)
        
        if time_keeping_user_count == 0:
            type_check = TypeCheckChoicesEnum.CHECKIN
        elif time_keeping_user_count == 1:
            type_check = TypeCheckChoicesEnum.CHECKOUT
        else:
            type_check = TypeCheckChoicesEnum.RAVAO
        
        # Tạo bản ghi mới
        time_keeping = Timekeeping(
            employee=user,
            check_type=type_check
        )
        time_keeping.save()
        
        # Cập nhật loại kiểm tra của các bản ghi từ bản ghi thứ hai đến bản ghi cuối cùng thành 'RAVAO'
        if time_keeping_user_count >= 2:
            # Lấy danh sách các bản ghi từ bản ghi thứ hai đến bản ghi cuối cùng
            middle_records = Timekeeping.objects.filter(
                employee=user,
                date=today
            ).order_by('id')[1:]
            # Cập nhật loại kiểm tra của từng bản ghi thành 'RAVAO'
            for record in middle_records:
                record.check_type = TypeCheckChoicesEnum.RAVAO
                record.save()
                # update_excel_file(user, TypeCheckChoicesEnum.RAVAO)
        
        # Lấy bản ghi cuối cùng
        
        last_record = Timekeeping.objects.filter(
            employee=user,
            date=today
        ).order_by('-id').first()
        # Đổi loại kiểm tra của bản ghi cuối cùng thành 'CHECKOUT'
        if time_keeping_user_count > 1:
            if last_record:
                last_record.check_type = TypeCheckChoicesEnum.CHECKOUT
                last_record.save()
                # update_excel_file(user, TypeCheckChoicesEnum.CHECKOUT)

        return time_keeping
    
    def to_representation(self, instance):
        
        representation = {
            'employee_id': instance.employee.id,
            'employee': instance.employee.first_name + " " + instance.employee.last_name,
            'department': instance.employee.department.name,
            'type_check': instance.check_type,
            'date_check': instance.date,
            'time_check': instance.check_time,

        }
        return representation
    
    def delete(self, instance):
        instance.delete()
