from django.urls import path
from .views import *

urlpatterns = [
    path('salary/getAll/', SalaryListView.as_view(), name='salary-get-all'),
    path('salary/create/', SalaryCreateView.as_view(), name='salary-create'),
    path('salary/delete/<int:pk>/', SalaryDeleteView.as_view(), name='salary-delete'),
    path('salary/delete-all/', SalaryDeleteAllView.as_view(), name='salary-delete-all'),
    path('profile/salary/', SalaryProfileView.as_view(), name='salary-profile'),
]
