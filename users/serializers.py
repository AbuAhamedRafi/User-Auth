from rest_framework import serializers
from authentication.models import User
from authentication.utils import validate_unique_email, validate_unique_username, validate_password_confirmation
from django.contrib.auth.password_validation import validate_password


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users (minimal information)
    """
    full_name = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'is_admin', 'is_active', 'created_at'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user information
    """
    full_name = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'is_admin', 'is_active', 
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users (Admin only)
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'role', 'is_active'
        ]
    
    def validate(self, attrs):
        """
        Validate password confirmation and other constraints
        """
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        validate_password_confirmation(password, password_confirm)
        validate_password(password)
        validate_unique_email(attrs.get('email'))
        validate_unique_username(attrs.get('username'))
        
        return attrs
    
    def create(self, validated_data):
        """
        Create user with hashed password
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information
    """
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'role', 'is_active'
        ]
    
    def validate_email(self, value):
        """
        Validate email uniqueness (excluding current user)
        """
        return validate_unique_email(value, exclude_pk=self.instance.pk)
    
    def validate_username(self, value):
        """
        Validate username uniqueness (excluding current user)
        """
        return validate_unique_username(value, exclude_pk=self.instance.pk)


class AdminUserStatsSerializer(serializers.Serializer):
    """
    Serializer for user statistics (Admin only)
    """
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    inactive_users = serializers.IntegerField()
    admin_users = serializers.IntegerField()
    moderator_users = serializers.IntegerField()
    regular_users = serializers.IntegerField()
    recent_registrations = serializers.IntegerField()
