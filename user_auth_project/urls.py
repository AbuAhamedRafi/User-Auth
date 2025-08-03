"""
URL configuration for user_auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """
    API Overview endpoint
    """
    return Response({
        'message': 'Welcome to User Authentication API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'refresh_token': '/api/auth/token/refresh/',
                'profile': '/api/auth/profile/',
                'change_password': '/api/auth/change-password/',
                'user_info': '/api/auth/user-info/',
            },
            'users': {
                'list_create': '/api/users/',
                'detail': '/api/users/{id}/',
                'stats': '/api/users/stats/',
                'toggle_status': '/api/users/{id}/toggle-status/',
            }
        },
        'authentication': 'JWT Bearer Token',
        'roles': ['admin', 'user']
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_overview, name='api_overview'),
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
]
