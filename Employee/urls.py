from django.urls import path
from .views import *

urlpatterns = [
    path('employees/getAll-filter/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/search/', EmployeeSearchListView.as_view(), name='employee-search'),
    path('profile/employee', EmployeeProfileView.as_view(), name='employee-profile'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/admin-update/<int:pk>/', EmployeeUpdateAdminView.as_view(), name='employee-admin-update'),
    path('employees/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-delete'),
]
