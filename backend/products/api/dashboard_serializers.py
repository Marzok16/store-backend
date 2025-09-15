from rest_framework import serializers
from ..models import Product, Category, Review
from users.models import User


class DashboardCategorySerializer(serializers.ModelSerializer):
    """
    Enhanced category serializer for dashboard with product count
    """
    product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']


class DashboardProductSerializer(serializers.ModelSerializer):
    """
    Enhanced product serializer for dashboard with additional fields
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    is_out_of_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'unit_price', 'image', 'stock',
            'date_added', 'category', 'category_name', 'average_rating',
            'review_count', 'is_low_stock', 'is_out_of_stock'
        ]
        read_only_fields = ['date_added', 'category_name', 'average_rating', 
                           'review_count', 'is_low_stock', 'is_out_of_stock']
    
    def get_review_count(self, obj):
        return obj.reviews.count()
    
    def get_is_low_stock(self, obj):
        return obj.stock > 0 and obj.stock <= 10
    
    def get_is_out_of_stock(self, obj):
        return obj.stock == 0
    
    def to_representation(self, instance):
        """
        Customize the output representation for GET requests
        """
        representation = super().to_representation(instance)
        
        # Handle image URL - return full URL if image exists
        if instance.image:
            request = self.context.get('request')
            if request:
                representation['image'] = request.build_absolute_uri(instance.image.url)
        
        return representation


class DashboardReviewSerializer(serializers.ModelSerializer):
    """
    Enhanced review serializer for dashboard with user and product info
    """
    user_name = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'title', 'content', 'rating', 'created_at',
            'user', 'user_name', 'user_email', 'product_id', 'product_title'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'user_name', 
                           'user_email', 'product_id', 'product_title']
    
    def get_user_name(self, obj):
        if obj.user:
            if obj.user.first_name or obj.user.last_name:
                return f"{obj.user.first_name} {obj.user.last_name}".strip()
            return obj.user.email
        return "Anonymous User"


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product creation and updates
    """
    class Meta:
        model = Product
        fields = ['title', 'description', 'unit_price', 'image', 'stock', 'category']
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
    
    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class BulkUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk product updates
    """
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="List of product IDs to update"
    )
    updates = serializers.DictField(
        help_text="Dictionary of fields to update"
    )
    
    def validate_product_ids(self, value):
        # Check if all product IDs exist
        existing_ids = Product.objects.filter(id__in=value).values_list('id', flat=True)
        missing_ids = set(value) - set(existing_ids)
        if missing_ids:
            raise serializers.ValidationError(
                f"Products with IDs {list(missing_ids)} do not exist"
            )
        return value
    
    def validate_updates(self, value):
        allowed_fields = ['stock', 'unit_price', 'category']
        for field in value.keys():
            if field not in allowed_fields:
                raise serializers.ValidationError(
                    f"Field '{field}' is not allowed for bulk update. "
                    f"Allowed fields: {allowed_fields}"
                )
        
        # Validate specific field values
        if 'stock' in value:
            if value['stock'] < 0:
                raise serializers.ValidationError("Stock cannot be negative")
        
        if 'unit_price' in value:
            if value['unit_price'] <= 0:
                raise serializers.ValidationError("Price must be greater than 0")
        
        if 'category' in value:
            try:
                Category.objects.get(id=value['category'])
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category does not exist")
        
        return value
