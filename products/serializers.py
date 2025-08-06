from rest_framework import serializers
from .models import Category, Product


class BasicUserSerializer(serializers.ModelSerializer):
    """
    Basic serializer for User information in foreign key relationships
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        from authentication.models import User
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    created_by = BasicUserSerializer(read_only=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'created_at', 'updated_at',
            'created_by', 'is_active', 'products_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_products_count(self, obj):
        """Get count of active products in this category"""
        return obj.products.filter(is_active=True).count()

    def create(self, validated_data):
        """Set the created_by field to current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating categories
    """
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']

    def create(self, validated_data):
        """Set the created_by field to current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    created_by = BasicUserSerializer(read_only=True)
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_id',
            'price', 'stock_quantity', 'sku', 'created_at', 'updated_at',
            'created_by', 'is_active', 'is_in_stock'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def validate_category_id(self, value):
        """Validate that the category exists and is active"""
        try:
            category = Category.objects.get(id=value, is_active=True)
            return value
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist or is inactive.")

    def create(self, validated_data):
        """Set the created_by field to current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating products
    """
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'price', 
            'stock_quantity', 'sku', 'is_active'
        ]

    def create(self, validated_data):
        """Set the created_by field to current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product listings
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'price', 
            'stock_quantity', 'sku', 'is_active', 'is_in_stock'
        ]
