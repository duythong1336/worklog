from django.urls import path
from .views import *

urlpatterns = [
    path('timekeeping/check-in-out/', CheckinCheckoutView.as_view(), name='timekeeping-check-in-out'),
    path('timekeeping/getAll-filter/', CheckinCheckoutListView.as_view(), name='timekeeping-list'),
    path('timekeeping/delete/<int:pk>/', TimeKeepingDeleteView.as_view(), name='timekeeping-delete'),
    path('profile/timekeeping/', TimekeepingProfileView.as_view(), name='timekeeping-profile-timekeeping'),
]
