from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from authentication.models import User
from authentication.permissions import IsAdminRole, IsOwnerOrAdmin
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)


class UserListCreateView(generics.ListCreateAPIView):
    """
    List all users or create a new user
    GET: Available to all authenticated users
    POST: Available only to Admin users
    """
    queryset = User.objects.all().order_by('-created_at')
    permission_classes = [IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [IsOwnerOrAdmin()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminRole()]
        return [IsOwnerOrAdmin()]
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        
        if user == request.user:
            return Response({
                'error': 'You cannot delete your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if not request.user.is_admin and 'role' in serializer.validated_data:
            if serializer.validated_data['role'] != instance.role:
                return Response({
                    'error': 'You cannot change your own role'
                }, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_update(serializer)
        return Response(UserDetailSerializer(instance).data, status=status.HTTP_200_OK)


class UserStatsView(generics.GenericAPIView):
    """
    Get user statistics (Admin only)
    """
    permission_classes = [IsAdminRole]
    
    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()
        admin_users = User.objects.filter(role='admin').count()
        moderator_users = User.objects.filter(role='moderator').count()
        regular_users = User.objects.filter(role='user').count()
        
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_registrations = User.objects.filter(created_at__gte=seven_days_ago).count()
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'admin_users': admin_users,
            'moderator_users': moderator_users,
            'regular_users': regular_users,
            'recent_registrations': recent_registrations,
        }, status=status.HTTP_200_OK)


class UserToggleStatusView(generics.GenericAPIView):
    """
    Toggle user active status (Admin only)
    """
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        if user == request.user:
            return Response({
                'error': 'You cannot deactivate your own account'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f'User has been {"activated" if user.is_active else "deactivated"}',
            'is_active': user.is_active
        }, status=status.HTTP_200_OK)
