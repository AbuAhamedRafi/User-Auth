from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    user_stats_view,
    toggle_user_status_view,
)

app_name = 'users'

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
    path('stats/', user_stats_view, name='user_stats'),
    path('<int:user_id>/toggle-status/', toggle_user_status_view, name='toggle_user_status'),
]
