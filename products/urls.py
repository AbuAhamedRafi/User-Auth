from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/stats/', views.CategoryStatsView.as_view(), name='category-stats'),
    path('categories/<int:pk>/toggle-status/', views.CategoryToggleStatusView.as_view(), name='toggle-category-status'),
    
    # Product URLs
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/stats/', views.ProductStatsView.as_view(), name='product-stats'),
    path('products/<int:pk>/toggle-status/', views.ProductToggleStatusView.as_view(), name='toggle-product-status'),
]
