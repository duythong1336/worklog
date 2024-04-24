from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from datetime import datetime
from openpyxl import load_workbook
from openpyxl import Workbook
import pandas as pd

import os.path

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


def format_respone(success, status, message, data):
    return {
        "success" : success,
        "status" : status,
        "message" : message,
        "data" : data, 
    }

def get_paginated_response(success, statusCode, message, totalItems, nextPage, previousPage, currentPage, totalPages, limit, data):
    return{
        "success": success,
        "statusCode": statusCode,
        "message": message,
        "totalItems": totalItems,
        "nextPage": nextPage,
        "previousPage": previousPage,
        "currentPage": currentPage,
        "totalPages": totalPages,
        "limit": limit,
        "data": data,
    }
    
def create_paginated_response(serializer, queryset, paginator, success=True, status_code=status.HTTP_200_OK):
    
    currentpage = paginator.page.number if paginator.page else None
    message = f"Get Page {currentpage} successfully"
    
    return get_paginated_response(
        success=success,
        statusCode=status_code,
        message=message,
        totalItems=queryset.count(),
        nextPage=paginator.page.next_page_number() if paginator.page and paginator.page.has_next() else None,
        previousPage=paginator.page.previous_page_number() if paginator.page and paginator.page.has_previous() else None,
        currentPage=currentpage,
        totalPages=paginator.page.paginator.num_pages if paginator.page else None,
        limit=paginator.page.paginator.per_page if paginator.page else None,
        data=serializer.data,
    )
    
def format_date(date):
    return date.strftime("%d-%m-%Y")

def update_excel_file(employee, check_type):
    file_path = 'check_in_out_records.xlsx'
    
    if os.path.exists(file_path):
        # Tệp đã tồn tại, mở nó để cập nhật

        wb = load_workbook(file_path)
        ws = wb.active
    else:
        # Tạo một workbook mới nếu tệp không tồn tại

        wb = Workbook()
        ws = wb.active
        ws.append(['Employee', 'Check Type', 'Date', 'Time'])

    # Thêm dữ liệu vào worksheet
    ws.append([employee.first_name + " " + employee.last_name , check_type, datetime.now().date(), datetime.now().time()])
    # Lưu workbook vào tệp Excel
    wb.save(file_path)



        
