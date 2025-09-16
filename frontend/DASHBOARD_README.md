# Store Dashboard

A React-based admin dashboard for managing your Amazon Clone store.

## Features

### 📊 Dashboard Overview
- Real-time statistics (total products, categories, reviews, stock status)
- Quick action buttons for common tasks
- Visual overview of store health

### 🛍️ Product Management
- **Add/Edit/Delete** products with image upload
- **Advanced filtering** by category, stock status, price range
- **Search functionality** across product titles and descriptions
- **Bulk operations** for updating multiple products
- **Stock management** with low stock alerts
- **Sorting options** (name, price, date, stock)

### 🏷️ Category Management
- **Create/Edit/Delete** categories
- **Product count** per category
- **Safe deletion** (prevents deleting categories with products)

### ⭐ Review Management
- **View all reviews** with filtering options
- **Delete inappropriate reviews**
- **Rating-based filtering**
- **Product-specific review filtering**

### 👥 User Management
- **List all users** with status information
- **Make users admin** with one click
- **User activity tracking**

## Getting Started

### Prerequisites
1. Make sure your Django backend is running on `http://localhost:8000`
2. Ensure you have an admin user account (`is_staff=True`)

### Accessing the Dashboard

1. **Login** to your account
2. **Navigate** to the dashboard:
   - Click "Store Dashboard" in the navbar (for admin users)
   - Or go directly to `/dashboard`
3. **Start managing** your store!

### Making a User Admin

If you need to make a user admin:

1. **Login as superuser** to Django admin
2. **Go to Users** section
3. **Edit the user** and check "Staff status"
4. **Save** the changes

Or use the API endpoint:
```bash
POST /api/users/admin/make-admin/
{
    "user_id": 1
}
```

## Dashboard Pages

### `/dashboard` - Overview
- Store statistics
- Quick action buttons
- Recent activity summary

### `/dashboard/products` - Product Management
- Product list with filtering
- Add/Edit/Delete products
- Bulk operations
- Image upload support

### `/dashboard/categories` - Category Management
- Category grid view
- Add/Edit/Delete categories
- Product count per category

### `/dashboard/reviews` - Review Management
- Review list with filtering
- Delete inappropriate reviews
- Rating and product filtering

### `/dashboard/users` - User Management
- User list with status
- Make users admin
- User activity information

## API Integration

The dashboard uses the following API endpoints:

- `GET /api/products/dashboard/stats/` - Dashboard statistics
- `GET /api/products/dashboard/products/` - Product list with filtering
- `POST /api/products/dashboard/products/create/` - Create product
- `PUT /api/products/dashboard/products/{id}/` - Update product
- `DELETE /api/products/dashboard/products/{id}/` - Delete product
- `GET /api/products/dashboard/categories/` - Category list
- `POST /api/products/dashboard/categories/` - Create category
- `GET /api/products/dashboard/reviews/` - Review list
- `DELETE /api/products/dashboard/reviews/{id}/delete/` - Delete review
- `GET /api/users/admin/users/` - User list
- `POST /api/users/admin/make-admin/` - Make user admin

## Security

- **Admin-only access** - All dashboard routes require `is_staff=True`
- **JWT authentication** - All API calls include authentication tokens
- **Protected routes** - React routes are protected with `AdminProtectedRoute`
- **Input validation** - All forms include client-side validation

## Responsive Design

The dashboard is fully responsive and works on:
- **Desktop** - Full sidebar navigation
- **Tablet** - Collapsible sidebar
- **Mobile** - Mobile-optimized layout

## Error Handling

- **API errors** are displayed as user-friendly messages
- **Loading states** for all async operations
- **Form validation** with real-time feedback
- **Network error handling** with retry options

## Development

### File Structure
```
src/
├── api/
│   └── dashboard.js          # Dashboard API service
├── components/
│   ├── dashboard/
│   │   └── DashboardLayout.jsx  # Main dashboard layout
│   └── AdminProtectedRoute.jsx  # Admin route protection
└── pages/
    └── dashboard/
        ├── DashboardOverview.jsx  # Overview page
        ├── ProductsPage.jsx       # Product management
        ├── CategoriesPage.jsx     # Category management
        ├── ReviewsPage.jsx        # Review management
        └── UsersPage.jsx          # User management
```

### Adding New Features

1. **Create API endpoint** in Django backend
2. **Add API service** in `src/api/dashboard.js`
3. **Create React component** in `src/pages/dashboard/`
4. **Add route** in `src/App.jsx`
5. **Update navigation** in `src/components/dashboard/DashboardLayout.jsx`

## Troubleshooting

### Common Issues

1. **"Access Denied" error**
   - Make sure your user has `is_staff=True`
   - Check if JWT token is valid

2. **API connection errors**
   - Verify Django server is running on port 8000
   - Check CORS settings in Django

3. **Image upload not working**
   - Ensure `MEDIA_ROOT` is configured in Django
   - Check file permissions

4. **Dashboard not loading**
   - Check browser console for errors
   - Verify all API endpoints are accessible

### Getting Help

1. Check the browser console for error messages
2. Verify API endpoints are working with the test script
3. Check Django server logs for backend errors
4. Ensure all dependencies are installed

## Future Enhancements

- **Real-time updates** with WebSocket integration
- **Advanced analytics** with charts and graphs
- **Export functionality** for products and orders
- **Bulk import** for products
- **Advanced user roles** and permissions
- **Audit logs** for admin actions


