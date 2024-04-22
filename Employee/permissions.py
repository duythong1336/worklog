from rest_framework.permissions import BasePermission

class IsAdminOrStaff(BasePermission):
    """
    Custom permission to allow only admins and staff members.
    """
    def has_permission(self, request, view):
        # Kiểm tra xem người dùng đã xác thực và là nhân viên hoặc là admin không
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)
    
