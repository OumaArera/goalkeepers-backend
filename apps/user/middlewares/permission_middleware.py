from rest_framework.permissions import BasePermission
from ...utils import has_permission


class IsVerifiedUser(BasePermission):
    """Permission for verified users only"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_verified and 
            not request.user.is_blocked
        )


class IsPlayer(BasePermission):
    """Permission for player only"""
    
    def has_permission(self, request, view):
        return has_permission(request.user, 'player')



class IsAdmin(BasePermission):
    """Permission for system administrators only"""
    
    def has_permission(self, request, view):
        return has_permission(request.user, 'admin') or request.user.is_superuser


class HasAnyRole(BasePermission):
    """Permission that accepts multiple roles"""
    
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles
    
    def has_permission(self, request, view):
        return has_permission(request.user, self.allowed_roles)
        
        
class AllUsers(BasePermission):
    """Permission for any authenticated user"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated