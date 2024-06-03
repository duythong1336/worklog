from django.urls import path
from .views import *

urlpatterns = [
    path('salary/get/all/', SalaryListView.as_view(), name='salary-get-all'),
    path('salary/create/', SalaryCreateView.as_view(), name='salary-create'),
    path('salary/delete/<int:pk>/', SalaryDeleteView.as_view(), name='salary-delete'),
    path('salary/delete-all/', SalaryDeleteAllView.as_view(), name='salary-delete-all'),
    path('profile/salary/', SalaryProfileView.as_view(), name='salary-profile'),
    path('salary/export/excel/', ExportSalaryExcel.as_view(), name='export_salary_excel'),
    path('salary/export/gsheet/', SalaryGoogleSheetView.as_view(), name='export_salary_gsheet'),
]
