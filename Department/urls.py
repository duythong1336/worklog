from django.urls import path
from .views import *

urlpatterns = [
    path('departments/getAll/', DepartmentListView.as_view(), name='department-list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department-create'),
    path('departments/update/<int:pk>/', DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/delete/<int:pk>/', DepartmentDeleteView.as_view(), name='department-delete'),
]
