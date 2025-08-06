from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from authentication.models import User
from authentication.permissions import IsAdminRole, IsOwnerOrAdmin
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    AdminUserStatsSerializer
)


class UserListCreateView(generics.ListCreateAPIView):
    """
    List all users or create a new user
    GET: Available to all authenticated users (limited info)
    POST: Available only to Admin users
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return users based on user role and filters
        """
        queryset = User.objects.all().order_by('-created_at')
        
        # Apply filters if provided
        search = self.request.query_params.get('search', None)
        role = self.request.query_params.get('role', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role=role)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on request method
        """
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer
    
    def get_permissions(self):
        """
        Set permissions based on request method
        """
        if self.request.method == 'POST':
            # Only admins can create users
            return [permissions.IsAuthenticated(), IsAdminRole()]
        return [permissions.IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user (Admin only)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User created successfully',
            'user': UserDetailSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user
    GET: Users can view their own profile, admins can view any profile
    PUT/PATCH: Users can update their own profile, admins can update any profile
    DELETE: Only admins can delete users
    """
    queryset = User.objects.all()
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on request method
        """
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def get_permissions(self):
        """
        Set permissions based on request method
        """
        if self.request.method == 'DELETE':
            # Only admins can delete users
            return [permissions.IsAuthenticated(), IsAdminRole()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a user (Admin only)
        """
        user = self.get_object()
        
        # Prevent admin from deleting themselves
        if user == request.user:
            return Response({
                'error': 'You cannot delete your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user_email = user.email
        user.delete()
        
        return Response({
            'message': f'User {user_email} deleted successfully'
        }, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        Update user information
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Prevent non-admin users from changing their role
        if not request.user.is_admin and 'role' in serializer.validated_data:
            if serializer.validated_data['role'] != instance.role:
                return Response({
                    'error': 'You cannot change your own role'
                }, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_update(serializer)
        
        return Response({
            'message': 'User updated successfully',
            'user': UserDetailSerializer(instance).data
        }, status=status.HTTP_200_OK)


class UserStatsView(generics.GenericAPIView):
    """
    Get user statistics (Admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    serializer_class = AdminUserStatsSerializer
    
    def get(self, request, *args, **kwargs):
        # Calculate statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()
        admin_users = User.objects.filter(role='admin').count()
        moderator_users = User.objects.filter(role='moderator').count()
        regular_users = User.objects.filter(role='user').count()
        
        # Recent registrations (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_registrations = User.objects.filter(created_at__gte=seven_days_ago).count()
        
        stats_data = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'admin_users': admin_users,
            'moderator_users': moderator_users,
            'regular_users': regular_users,
            'recent_registrations': recent_registrations,
        }
        
        serializer = self.get_serializer(stats_data)
        
        return Response({
            'stats': serializer.data
        }, status=status.HTTP_200_OK)


class UserToggleStatusView(generics.GenericAPIView):
    """
    Toggle user active status (Admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'pk'
    
    def post(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Prevent admin from deactivating themselves
        if user == request.user:
            return Response({
                'error': 'You cannot deactivate your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = not user.is_active
        user.save()
        
        status_text = 'activated' if user.is_active else 'deactivated'
        
        return Response({
            'message': f'User {user.email} has been {status_text}',
            'user': UserDetailSerializer(user).data
        }, status=status.HTTP_200_OK)
