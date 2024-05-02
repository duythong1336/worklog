from celery import shared_task
from .models import Salary
from Employee.models import Employee
from datetime import datetime, timedelta

@shared_task
def create_previous_month_salaries():
    # Lấy tháng và năm hiện tại
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Lấy tháng và năm của tháng trước
    previous_month = current_month - 1 if current_month != 1 else 12
    previous_year = current_year if current_month != 1 else current_year - 1
    
    # Lấy ngày đầu tiên và ngày cuối cùng của tháng trước
    start_date = datetime(previous_year, previous_month, 1)
    end_date = start_date.replace(month=previous_month % 12 + 1, day=1) - timedelta(days=1)
    
    # Lấy danh sách tất cả các nhân viên
    employees = Employee.objects.all()
    
    # Duyệt qua từng nhân viên và kiểm tra xem họ đã có bản ghi lương cho tháng trước chưa
    for employee in employees:
        # Kiểm tra xem nhân viên đã có bản ghi lương cho tháng trước chưa
        if not Salary.objects.filter(employee=employee, created_at__year=previous_year, created_at__month=previous_month).exists():
            # Nếu chưa có, tạo một bản ghi lương mới cho nhân viên đó
            salary = Salary(
                employee=employee,
                month=previous_month,
                year=previous_year
            )
            salary.save()
