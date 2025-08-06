from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    UserStatsView,
    UserToggleStatusView,
)

app_name = 'users'

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('stats/', UserStatsView.as_view(), name='user_stats'),
    path('<int:user_id>/toggle-status/', UserToggleStatusView.as_view(), name='toggle_user_status'),
]
