from rest_framework.permissions import BasePermission
from users.models import User


class IsTeacherAndVerified(BasePermission):
    """Faqat Teacher va tasdiqlangan userlar uchun permission"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_verified and
            request.user.roles == User.RolesTypes.TEACHER
        )
