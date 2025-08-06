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


class IsAdminOrModerator(permissions.BasePermission):
    """
    Permission class to check if user has admin or moderator role
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_moderator)
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


class IsOwnerOrAdminOrModerator(permissions.BasePermission):
    """
    Permission class to allow access to object owner, admin, or moderator
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_moderator:
            return True
        
        return obj == request.user or (hasattr(obj, 'user') and obj.user == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow read access to all users but write access only to admins
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_admin


class IsAdminOrModeratorForProducts(permissions.BasePermission):
    """
    Permission class for products:
    - Admins & Moderators: Full CRUD access
    - Users: Read-only access
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Allow read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write access for admins and moderators
        return request.user.is_admin or request.user.is_moderator
