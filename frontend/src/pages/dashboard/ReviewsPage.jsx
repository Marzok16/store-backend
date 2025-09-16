import { useState, useEffect } from 'react';
import { dashboardAPI } from '../../api/dashboard';
import {
  TrashIcon,
  MagnifyingGlassIcon,
  StarIcon,
} from '@heroicons/react/24/outline';

const ReviewsPage = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    rating: '',
    product: ''
  });

  useEffect(() => {
    fetchReviews();
  }, [filters]);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const response = await dashboardAPI.getReviews(filters);
      setReviews(response.data.results || []);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch reviews');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this review?')) {
      try {
        await dashboardAPI.deleteReview(id);
        fetchReviews();
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to delete review');
      }
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <StarIcon
        key={i}
        className={`h-4 w-4 ${
          i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Reviews</h1>
        <p className="mt-1 text-sm text-gray-500">
          Manage customer reviews
        </p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Filters */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Search</label>
            <div className="mt-1 relative">
              <MagnifyingGlassIcon className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
              <input
                type="text"
                value={filters.search}
                onChange={(e) => setFilters({...filters, search: e.target.value})}
                className="pl-10 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                placeholder="Search reviews..."
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Rating</label>
            <select
              value={filters.rating}
              onChange={(e) => setFilters({...filters, rating: e.target.value})}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Ratings</option>
              <option value="5">5 Stars</option>
              <option value="4">4 Stars</option>
              <option value="3">3 Stars</option>
              <option value="2">2 Stars</option>
              <option value="1">1 Star</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Product ID</label>
            <input
              type="number"
              value={filters.product}
              onChange={(e) => setFilters({...filters, product: e.target.value})}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Filter by product ID"
            />
          </div>
        </div>
      </div>

      {/* Reviews List */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {reviews.map((review) => (
            <li key={review.id} className="px-4 py-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <h4 className="text-sm font-medium text-gray-900">{review.title}</h4>
                      <div className="ml-2 flex">
                        {renderStars(review.rating)}
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">
                      {new Date(review.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <p className="mt-2 text-sm text-gray-600">{review.content}</p>
                  <div className="mt-3 flex items-center text-sm text-gray-500">
                    <span>By: {review.user_name}</span>
                    <span className="mx-2">•</span>
                    <span>Product: {review.product_title}</span>
                  </div>
                </div>
                <div className="ml-4 flex-shrink-0">
                  <button
                    onClick={() => handleDelete(review.id)}
                    className="text-red-600 hover:text-red-900"
                    title="Delete review"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
        {reviews.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No reviews found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReviewsPage;


