import axios from './axios';

// Dashboard API service for product management
export const dashboardAPI = {
  // Dashboard Statistics
  getStats: () => axios.get('/products/dashboard/stats/'),

  // Product Management
  getProducts: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return axios.get(`/products/dashboard/products/?${queryParams.toString()}`);
  },

  createProduct: (productData) => {
    const formData = new FormData();
    Object.keys(productData).forEach(key => {
      if (productData[key] !== undefined && productData[key] !== null) {
        formData.append(key, productData[key]);
      }
    });
    return axios.post('/products/dashboard/products/create/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getProduct: (id) => axios.get(`/products/dashboard/products/${id}/`),
  updateProduct: (id, productData) => {
    const formData = new FormData();
    Object.keys(productData).forEach(key => {
      if (productData[key] !== undefined && productData[key] !== null) {
        formData.append(key, productData[key]);
      }
    });
    return axios.put(`/products/dashboard/products/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  deleteProduct: (id) => axios.delete(`/products/dashboard/products/${id}/`),
  bulkUpdateProducts: (productIds, updates) => 
    axios.post('/products/dashboard/products/bulk-update/', {
      product_ids: productIds,
      updates: updates
    }),

  // Category Management
  getCategories: () => axios.get('/products/dashboard/categories/'),
  createCategory: (categoryData) => axios.post('/products/dashboard/categories/', categoryData),
  getCategory: (id) => axios.get(`/products/dashboard/categories/${id}/`),
  updateCategory: (id, categoryData) => axios.put(`/products/dashboard/categories/${id}/`, categoryData),
  deleteCategory: (id) => axios.delete(`/products/dashboard/categories/${id}/`),

  // Review Management
  getReviews: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });
    return axios.get(`/products/dashboard/reviews/?${queryParams.toString()}`);
  },
  deleteReview: (id) => axios.delete(`/products/dashboard/reviews/${id}/delete/`),

  // User Management
  getUsers: () => axios.get('/users/admin/users/'),
  makeUserAdmin: (userId) => axios.post('/users/admin/make-admin/', { user_id: userId }),
};


