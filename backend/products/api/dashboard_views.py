from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Avg
from django.db import models
from ..models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .dashboard_serializers import (
    DashboardProductSerializer, DashboardCategorySerializer, 
    DashboardReviewSerializer, ProductCreateUpdateSerializer,
    BulkUpdateSerializer
)
from users.models import User


class DashboardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin users
    """
    # Check if user is admin (you can customize this logic)
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    stats = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_reviews': Review.objects.count(),
        'products_with_stock': Product.objects.filter(stock__gt=0).count(),
        'products_out_of_stock': Product.objects.filter(stock=0).count(),
        'average_rating': Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
        'recent_products': Product.objects.filter(
            date_added__gte=models.DateTimeField().now().replace(day=1)
        ).count()
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_products(request):
    """
    Get all products with advanced filtering for dashboard
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    products = Product.objects.select_related('category').prefetch_related('reviews')
    
    # Search functionality
    search_query = request.query_params.get('search')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.query_params.get('category')
    if category_id:
        try:
            products = products.filter(category_id=int(category_id))
        except ValueError:
            return Response(
                {"error": "Invalid category ID"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Filter by stock status
    stock_filter = request.query_params.get('stock')
    if stock_filter == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(stock=0)
    elif stock_filter == 'low_stock':
        products = products.filter(stock__gt=0, stock__lte=10)
    
    # Filter by price range
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    if min_price:
        try:
            products = products.filter(unit_price__gte=float(min_price))
        except ValueError:
            return Response(
                {"error": "Invalid min_price"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    if max_price:
        try:
            products = products.filter(unit_price__lte=float(max_price))
        except ValueError:
            return Response(
                {"error": "Invalid max_price"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Sorting
    sort_by = request.query_params.get('sort', '-date_added')
    valid_sorts = ['title', '-title', 'unit_price', '-unit_price', 'stock', '-stock', 'date_added', '-date_added']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-date_added')
    
    # Pagination
    paginator = DashboardPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = DashboardProductSerializer(paginated_products, many=True, context={'request': request})
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    """
    Create a new product (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = ProductCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        # Return the full product data with dashboard serializer
        response_serializer = DashboardProductSerializer(product, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_product(request, product_id):
    """
    Get, update, or delete a specific product (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = DashboardProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ProductCreateUpdateSerializer(
            product, 
            data=request.data, 
            partial=partial
        )
        if serializer.is_valid():
            product = serializer.save()
            # Return the full product data with dashboard serializer
            response_serializer = DashboardProductSerializer(product, context={'request': request})
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_categories(request):
    """
    Get all categories or create a new one (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        categories = Category.objects.annotate(
            product_count=Count('products')
        ).order_by('name')
        serializer = DashboardCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DashboardCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_category(request, category_id):
    """
    Get, update, or delete a specific category (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = DashboardCategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Check if category has products
        if category.products.exists():
            return Response(
                {"error": "Cannot delete category with existing products"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = DashboardCategorySerializer(category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_reviews(request):
    """
    Get all reviews with filtering for dashboard (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    reviews = Review.objects.select_related('user', 'product').order_by('-created_at')
    
    # Filter by rating
    rating = request.query_params.get('rating')
    if rating:
        try:
            rating_int = int(rating)
            if 1 <= rating_int <= 5:
                reviews = reviews.filter(rating=rating_int)
        except ValueError:
            return Response(
                {"error": "Invalid rating"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Filter by product
    product_id = request.query_params.get('product')
    if product_id:
        try:
            reviews = reviews.filter(product_id=int(product_id))
        except ValueError:
            return Response(
                {"error": "Invalid product ID"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Search in review content
    search = request.query_params.get('search')
    if search:
        reviews = reviews.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search)
        )
    
    # Pagination
    paginator = DashboardPagination()
    paginated_reviews = paginator.paginate_queryset(reviews, request)
    serializer = DashboardReviewSerializer(paginated_reviews, many=True)
    
    return paginator.get_paginated_response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """
    Delete a specific review (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return Response(
            {"error": "Review not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_products(request):
    """
    Bulk update products (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = BulkUpdateSerializer(data=request.data)
    if serializer.is_valid():
        product_ids = serializer.validated_data['product_ids']
        updates = serializer.validated_data['updates']
        
        # Update products
        updated_count = Product.objects.filter(id__in=product_ids).update(**updates)
        
        return Response({
            "message": f"Successfully updated {updated_count} products",
            "updated_count": updated_count
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
