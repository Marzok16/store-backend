# Dashboard API Documentation

This document describes the dashboard API endpoints for managing products, categories, and reviews in the Amazon Clone store.

## Authentication

All dashboard endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Admin Access

Most dashboard endpoints require admin privileges (`is_staff=True`). To make a user admin, use the admin endpoint:

```
POST /api/users/admin/make-admin/
{
    "user_id": 1
}
```

## Base URL

All dashboard endpoints are prefixed with `/api/products/dashboard/`

## Endpoints

### 1. Dashboard Statistics

**GET** `/api/products/dashboard/stats/`

Returns overall statistics for the dashboard.

**Response:**
```json
{
    "total_products": 150,
    "total_categories": 12,
    "total_reviews": 89,
    "products_with_stock": 120,
    "products_out_of_stock": 30,
    "average_rating": 4.2,
    "recent_products": 15
}
```

### 2. Product Management

#### Get All Products (Dashboard)

**GET** `/api/products/dashboard/products/`

**Query Parameters:**
- `search` - Search in title, description, or category name
- `category` - Filter by category ID
- `stock` - Filter by stock status (`in_stock`, `out_of_stock`, `low_stock`)
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `sort` - Sort by field (`title`, `-title`, `unit_price`, `-unit_price`, `stock`, `-stock`, `date_added`, `-date_added`)
- `page` - Page number for pagination
- `page_size` - Items per page (max 100)

**Response:**
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/products/dashboard/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "iPhone 15 Pro",
            "description": "Latest iPhone with advanced features",
            "unit_price": "999.99",
            "image": "http://localhost:8000/media/products/iphone15.jpg",
            "stock": 25,
            "date_added": "2024-01-15T10:30:00Z",
            "category": 1,
            "category_name": "Electronics",
            "average_rating": 4.5,
            "review_count": 12,
            "is_low_stock": false,
            "is_out_of_stock": false
        }
    ]
}
```

#### Create Product

**POST** `/api/products/dashboard/products/create/`

**Request Body:**
```json
{
    "title": "New Product",
    "description": "Product description",
    "unit_price": "99.99",
    "stock": 50,
    "category": 1,
    "image": "<file_upload>"
}
```

#### Get/Update/Delete Product

**GET/PUT/PATCH/DELETE** `/api/products/dashboard/products/{product_id}/`

- **GET**: Retrieve product details
- **PUT**: Update entire product
- **PATCH**: Partial update
- **DELETE**: Delete product

#### Bulk Update Products

**POST** `/api/products/dashboard/products/bulk-update/`

**Request Body:**
```json
{
    "product_ids": [1, 2, 3],
    "updates": {
        "stock": 100,
        "unit_price": "89.99"
    }
}
```

### 3. Category Management

#### Get All Categories

**GET** `/api/products/dashboard/categories/`

**Response:**
```json
[
    {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and gadgets",
        "product_count": 45
    }
]
```

#### Create Category

**POST** `/api/products/dashboard/categories/`

**Request Body:**
```json
{
    "name": "New Category",
    "description": "Category description"
}
```

#### Get/Update/Delete Category

**GET/PUT/PATCH/DELETE** `/api/products/dashboard/categories/{category_id}/`

- **GET**: Retrieve category details
- **PUT**: Update entire category
- **PATCH**: Partial update
- **DELETE**: Delete category (only if no products exist)

### 4. Review Management

#### Get All Reviews

**GET** `/api/products/dashboard/reviews/`

**Query Parameters:**
- `rating` - Filter by rating (1-5)
- `product` - Filter by product ID
- `search` - Search in title or content
- `page` - Page number
- `page_size` - Items per page

**Response:**
```json
{
    "count": 89,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Great product!",
            "content": "Really happy with this purchase",
            "rating": 5,
            "created_at": "2024-01-15T10:30:00Z",
            "user": 1,
            "user_name": "John Doe",
            "user_email": "john@example.com",
            "product_id": 1,
            "product_title": "iPhone 15 Pro"
        }
    ]
}
```

#### Delete Review

**DELETE** `/api/products/dashboard/reviews/{review_id}/delete/`

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

```json
{
    "error": "Admin access required"
}
```

Common status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `204` - No Content (for deletions)

## Usage Examples

### Creating a Product with Image Upload

```javascript
const formData = new FormData();
formData.append('title', 'New Product');
formData.append('description', 'Product description');
formData.append('unit_price', '99.99');
formData.append('stock', '50');
formData.append('category', '1');
formData.append('image', fileInput.files[0]);

fetch('/api/products/dashboard/products/create/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + token
    },
    body: formData
});
```

### Bulk Updating Product Stock

```javascript
fetch('/api/products/dashboard/products/bulk-update/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        product_ids: [1, 2, 3],
        updates: {
            stock: 100
        }
    })
});
```

## Frontend Integration

The dashboard API is designed to work seamlessly with React frontend applications. Key features:

1. **Pagination**: All list endpoints support pagination
2. **Filtering**: Advanced filtering options for products and reviews
3. **Search**: Full-text search capabilities
4. **Image Upload**: Support for product image uploads
5. **Bulk Operations**: Efficient bulk update operations
6. **Real-time Stats**: Dashboard statistics for overview

## Security

- All endpoints require authentication
- Admin endpoints require `is_staff=True`
- Input validation on all endpoints
- File upload restrictions (images only)
- SQL injection protection through Django ORM
