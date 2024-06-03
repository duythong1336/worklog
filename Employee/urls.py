from django.urls import path
from .views import *

urlpatterns = [
    path('employees/get/all/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeGetOneView.as_view(), name='employee-get-one'),
    path('profile/employee', EmployeeProfileView.as_view(), name='employee-profile'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/admin-update/<int:pk>/', EmployeeUpdateAdminView.as_view(), name='employee-admin-update'),
    path('employees/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('profile/employees/change-password/send-mail/', ChangePasswordRequestAPIView.as_view(), name='employee-change-password-send-mail'),
    path('profile/employees/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('profile/employees/change-password/new-password/', NewPasswordAPIView.as_view(), name='employee-change-password-new-password'),
    path('employees/forgot/password/', ForgotPassView.as_view(), name='employee-forgot-password'),
]
