from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/getAll/', JWTTokenListView.as_view(), name='token-get-all'),
    path('token/get-by-user/', JWTTokenByUserListView.as_view(), name='token-get-all-by-user-id'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
    path('logout-1-or-many/', LogoutDevicesView.as_view(), name='logout-1-or-many'),
]
