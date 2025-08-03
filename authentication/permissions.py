from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Permission class to check if user has admin role
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_admin
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class to allow access to object owner or admin
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        
        return obj == request.user or (hasattr(obj, 'user') and obj.user == request.user)


class IsUserRole(permissions.BasePermission):
    """
    Permission class to check if user has user role
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_regular_user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow read access to all users but write access only to admins
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_admin
        )
