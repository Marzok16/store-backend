from django.urls import path
from . import dashboard_views

urlpatterns = [
    # Dashboard statistics
    path('stats/', dashboard_views.dashboard_stats, name='dashboard-stats'),
    
    # Product management
    path('products/', dashboard_views.dashboard_products, name='dashboard-products'),
    path('products/create/', dashboard_views.create_product, name='create-product'),
    path('products/<int:product_id>/', dashboard_views.manage_product, name='manage-product'),
    path('products/bulk-update/', dashboard_views.bulk_update_products, name='bulk-update-products'),
    
    # Category management
    path('categories/', dashboard_views.manage_categories, name='manage-categories'),
    path('categories/<int:category_id>/', dashboard_views.manage_category, name='manage-category'),
    
    # Review management
    path('reviews/', dashboard_views.dashboard_reviews, name='dashboard-reviews'),
    path('reviews/<int:review_id>/delete/', dashboard_views.delete_review, name='delete-review'),
]
