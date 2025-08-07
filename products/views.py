from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Avg

from .models import Category, Product
from .serializers import (
    CategorySerializer, CategoryCreateSerializer,
    ProductSerializer, ProductCreateSerializer, ProductListSerializer
)
from authentication.permissions import (
    IsAdminOrModerator, IsAdminOrModeratorForProducts
)


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    Admins and moderators can access categories.
    """
    queryset = Category.objects.filter(is_active=True)
    permission_classes = [IsAdminOrModerator]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category.
    Admins and moderators can access categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrModerator]

    def destroy(self, request, *args, **kwargs):
        """Soft delete by setting is_active to False"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    Admins and Moderators: Full access
    Users: Read-only access
    """
    queryset = Product.objects.filter(is_active=True).select_related('category', 'created_by')
    permission_classes = [IsAdminOrModeratorForProducts]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku', 'category__name']
    ordering_fields = ['id', 'name', 'price', 'created_at', 'stock_quantity']
    ordering = ['id']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        """Filter products based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by stock status
        in_stock = self.request.query_params.get('in_stock')
        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_quantity=0)
        
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product.
    Admins and Moderators: Full access
    Users: Read-only access
    """
    queryset = Product.objects.select_related('category', 'created_by')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrModeratorForProducts]

    def destroy(self, request, *args, **kwargs):
        """Soft delete by setting is_active to False"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Additional API Views
class CategoryStatsView(generics.GenericAPIView):
    """
    Get category statistics (Admin and Moderator only)
    """
    permission_classes = [IsAdminOrModerator]
    
    def get(self, request):
        categories = Category.objects.all()
        stats = {
            'total_categories': categories.count(),
            'active_categories': categories.filter(is_active=True).count(),
            'inactive_categories': categories.filter(is_active=False).count(),
            'categories_with_products': categories.filter(products__isnull=False).distinct().count(),
        }
        
        return Response({'stats': stats})


class ProductStatsView(generics.GenericAPIView):
    """
    Get product statistics 
    Admins and Moderators: Full stats
    Users: Basic stats only
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.all()
        basic_stats = {
            'total_products': products.filter(is_active=True).count(),
            'products_in_stock': products.filter(is_active=True, stock_quantity__gt=0).count(),
            'products_out_of_stock': products.filter(is_active=True, stock_quantity=0).count(),
        }
        
        if request.user.is_admin or request.user.is_moderator:
            # Additional stats for admins and moderators
            admin_stats = {
                'total_products_including_inactive': products.count(),
                'inactive_products': products.filter(is_active=False).count(),
                'categories_count': Category.objects.filter(is_active=True).count(),
                'average_price': products.filter(is_active=True).aggregate(
                    avg_price=Avg('price')
                )['avg_price'] or 0,
            }
            basic_stats.update(admin_stats)
        
        return Response({'stats': basic_stats})


class CategoryToggleStatusView(generics.GenericAPIView):
    """
    Toggle category active status (Admin and Moderator only)
    """
    permission_classes = [IsAdminOrModerator]
    
    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.is_active = not category.is_active
            category.save()
            
            return Response({
                'message': f'Category status updated to {"active" if category.is_active else "inactive"}',
                'is_active': category.is_active
            })
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ProductToggleStatusView(generics.GenericAPIView):
    """
    Toggle product active status (Admin and Moderator only)
    """
    permission_classes = [IsAdminOrModeratorForProducts]
    
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.is_active = not product.is_active
            product.save()
            
            return Response({
                'message': f'Product status updated to {"active" if product.is_active else "inactive"}',
                'is_active': product.is_active
            })
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
