"""
Utility functions for authentication app
"""
from rest_framework import serializers
from .models import User


def validate_unique_email(email, exclude_pk=None):
    """
    Validate that email is unique, optionally excluding a specific user
    """
    queryset = User.objects.filter(email=email)
    if exclude_pk:
        queryset = queryset.exclude(pk=exclude_pk)
    
    if queryset.exists():
        raise serializers.ValidationError("User with this email already exists.")
    return email


def validate_unique_username(username, exclude_pk=None):
    """
    Validate that username is unique, optionally excluding a specific user
    """
    queryset = User.objects.filter(username=username)
    if exclude_pk:
        queryset = queryset.exclude(pk=exclude_pk)
    
    if queryset.exists():
        raise serializers.ValidationError("Username already exists.")
    return username


def validate_password_confirmation(password, password_confirm):
    """
    Validate that password and password confirmation match
    """
    if password != password_confirm:
        raise serializers.ValidationError("Passwords don't match.")
    return password
