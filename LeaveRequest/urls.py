from django.urls import path
from .views import *

urlpatterns = [
    path('LeaveRequest/get/all/', LeaveRequestListView.as_view(), name='LeaveRequest-get-all'),
    path('LeaveRequest/create/', LeaveRequestCreateView.as_view(), name='LeaveRequest-create'),
    path('LeaveRequest/approved/<int:pk>/', ApprovedStatusView.as_view(), name='LeaveRequest-approved'),
    path('LeaveRequest/rejected/<int:pk>/', RejectedStatusView.as_view(), name='LeaveRequest-rejected'),
    # path('LeaveRequest/search/', LeaveRequestSearchView.as_view(), name='LeaveRequest-search'),
    path('LeaveRequest/delete/<int:pk>/', LeaveRequestDeleteView.as_view(), name='LeaveRequest-delete'),
    path('profile/LeaveRequest/', LeaveRequestProfileView.as_view(), name='LeaveRequest-profile'),
]
