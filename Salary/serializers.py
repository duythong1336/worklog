from rest_framework import serializers
from Employee.models import Employee
from LeaveRequest.models import LeaveRequest, StatusChoicesEnum
from .models import Salary
from Timekeeping.models import Timekeeping
from django.core.mail import send_mail
from datetime import datetime, timedelta
import calendar
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from share.utils import update_google_sheet_salary

class SalarySerializer(serializers.Serializer):
    
    def create(self, validated_data):
        self.create_previous_month_salaries()
        return Employee.objects.all()

    def create_previous_month_salaries(self):
        # Lấy tháng và năm hiện tại
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Lấy tháng và năm của tháng trước
        previous_month = current_month - 1 if current_month != 1 else 12
        previous_year = current_year if current_month != 1 else current_year - 1
        
        num_days_in_previous_month = calendar.monthrange(previous_year, previous_month)[1]

        # Đếm số ngày là thứ 7 và Chủ nhật
        count_weekend_days = sum(1 for day in range(1, num_days_in_previous_month + 1) if calendar.weekday(previous_year, previous_month, day) in [calendar.SATURDAY, calendar.SUNDAY])
        
        
        
        # Lấy danh sách tất cả các nhân viên
        employees = Employee.objects.all()
        
        # Duyệt qua từng nhân viên và kiểm tra xem họ đã có bản ghi lương cho tháng trước chưa
        for employee in employees:
            # Kiểm tra xem nhân viên đã có bản ghi lương cho tháng trước chưa
            if not Salary.objects.filter(employee=employee, year=previous_year, month=previous_month).exists():
                # Nếu chưa có, tạo một bản ghi lương mới cho nhân viên đó
                total_workdays = self.calculate_total_workdays(employee, previous_month, previous_year)
                total_leave_days = self.calculate_total_leave_days(employee, previous_month, previous_year)
                num_days_without_weekend = num_days_in_previous_month - count_weekend_days
                total_salary = self.calculate_total_salary(employee, total_workdays, previous_month, previous_year, num_days_without_weekend, total_leave_days)
                
                salary = Salary(
                    employee=employee,
                    month=previous_month,
                    year=previous_year,
                    total_salary = total_salary,
                    created_at = datetime.now()
                    
                )
                salary.save()
                # update_google_sheet_salary()
                # update_google_sheet_salary(employee, total_workdays, total_leave_days, total_salary, previous_month, previous_year)
                
    def calculate_total_workdays(self, employee, previous_month, previous_year):

        # Lấy ngày đầu tiên và ngày cuối cùng của tháng trước
        start_date = datetime(previous_year, previous_month, 1)
        end_date = start_date.replace(month=previous_month % 12 + 1, day=1) - timedelta(days=1)
        
        # Tính toán số ngày làm việc trong tháng trước
        total_workdays = 0
        for day in range(1, end_date.day + 1):
            checkin_exists = Timekeeping.objects.filter(
                employee=employee,
                date__year=previous_year,
                date__month=previous_month,
                date__day=day,
                check_type='CHECKIN'
            ).exists()
            checkout_exists = Timekeeping.objects.filter(
                employee=employee,
                date__year=previous_year,
                date__month=previous_month,
                date__day=day,
                check_type='CHECKOUT'
            ).exists()
            if checkin_exists and checkout_exists:
                total_workdays += 1
        
        return total_workdays
    
    def calculate_total_salary(self, employee, total_workdays, previous_month, previous_year, num_days_without_weekend, total_leave_days):
        # Lấy lương của nhân viên
        salary_per_month = employee.salary

        # Chuyển đổi total_workdays thành decimal.Decimal
        total_workdays_decimal = Decimal(total_workdays)
        
        salary_one_day = salary_per_month * Decimal(1 / num_days_without_weekend)
        
        # Tính tổng lương
        if total_leave_days >= 2 and total_workdays >= 1:
            total_salary = salary_per_month * (total_workdays_decimal / num_days_without_weekend) + salary_one_day
        else:
            total_salary = salary_per_month * (total_workdays_decimal / num_days_without_weekend)
        
        return total_salary
    
    # def calculate_total_leave_days(self, employee, total_workdays, previous_month, previous_year, num_days_in_previous_month):
    #     # Tính số ngày nghỉ bằng cách lấy số ngày của tháng trước trừ đi số ngày làm việc
    #     total_leave_days = num_days_in_previous_month - total_workdays
        
    #     return total_leave_days
    
    def calculate_total_leave_days(self, employee, previous_month, previous_year):
        # Tạo một tập hợp để lưu trữ các ngày đã tính
        counted_days = set()

        # Truy vấn yêu cầu nghỉ phép của nhân viên trong tháng trước
        leave_requests = LeaveRequest.objects.filter(employee=employee, start_date__month=previous_month, start_date__year=previous_year, status=StatusChoicesEnum.APPROVED)

        total_leave_days = 0
        for leave_request in leave_requests:
            # Lặp qua từng ngày trong khoảng thời gian của yêu cầu nghỉ phép
            current_date = leave_request.start_date
            while current_date <= leave_request.end_date:
                # Kiểm tra nếu ngày hiện tại chưa được tính trước đó
                if current_date not in counted_days:
                    total_leave_days += 1
                    counted_days.add(current_date)  # Thêm ngày vào tập hợp đã tính
                current_date += timedelta(days=1)  # Di chuyển sang ngày tiếp theo trong khoảng thời gian yêu cầu nghỉ phép

        return total_leave_days
    
    
    def to_representation(self, instance):
        
        # Lấy tháng và năm của tháng trước
        current_month = datetime.now().month
        current_year = datetime.now().year
        previous_month = current_month - 1 if current_month != 1 else 12
  
        
        previous_year = current_year if current_month != 1 else current_year - 1
        
        # Lấy số ngày trong tháng trước
        num_days_in_previous_month = calendar.monthrange(previous_year, previous_month)[1]

        # Đếm số ngày là thứ 7 và Chủ nhật
        count_weekend_days = sum(1 for day in range(1, num_days_in_previous_month + 1) if calendar.weekday(previous_year, previous_month, day) in [calendar.SATURDAY, calendar.SUNDAY])

        # Tổng số ngày trong tháng trước loại bỏ các ngày là thứ 7 và Chủ nhật
        num_days_without_weekend = num_days_in_previous_month - count_weekend_days
        # print(num_days_in_previous_month)
        # print(count_weekend_days)
        # print(num_days_without_weekend)
        total_workdays = self.calculate_total_workdays(instance.employee, previous_month, previous_year)
        total_leave_days = self.calculate_total_leave_days(instance.employee, previous_month, previous_year)
        # total_salary = self.calculate_total_salary(instance.employee, total_workdays, previous_month, previous_year, num_days_without_weekend, total_leave_days)
        
        representation = {
            'id': instance.id,
            'employee_fullname': instance.employee.first_name + " " + instance.employee.last_name,
            'salary_month': instance.month,
            'salary_year': instance.year,
            'total_workdays': total_workdays,
            'total_leave_days': total_leave_days,
            'total_salary': int(instance.total_salary),
            
        }
        return representation

    def delete(self, instance):
        instance.delete()