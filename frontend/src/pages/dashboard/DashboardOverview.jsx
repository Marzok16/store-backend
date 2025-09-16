import { useState, useEffect } from 'react';
import { dashboardAPI } from '../../api/dashboard';
import {
  ShoppingBagIcon,
  TagIcon,
  ChatBubbleLeftRightIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';

const DashboardOverview = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await dashboardAPI.getStats();
      setStats(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch dashboard statistics');
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">{error}</div>
          </div>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      name: 'Total Products',
      value: stats?.total_products || 0,
      icon: ShoppingBagIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Categories',
      value: stats?.total_categories || 0,
      icon: TagIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Reviews',
      value: stats?.total_reviews || 0,
      icon: ChatBubbleLeftRightIcon,
      color: 'bg-yellow-500',
    },
    {
      name: 'In Stock',
      value: stats?.products_with_stock || 0,
      icon: CheckCircleIcon,
      color: 'bg-emerald-500',
    },
    {
      name: 'Out of Stock',
      value: stats?.products_out_of_stock || 0,
      icon: ExclamationTriangleIcon,
      color: 'bg-red-500',
    },
    {
      name: 'Avg Rating',
      value: stats?.average_rating ? stats.average_rating.toFixed(1) : '0.0',
      icon: ChatBubbleLeftRightIcon,
      color: 'bg-purple-500',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome to your store management dashboard
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
          >
            <dt>
              <div className={`absolute rounded-md p-3 ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline">
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            </dd>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <a
            href="/dashboard/products"
            className="relative block rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <ShoppingBagIcon className="mx-auto h-8 w-8 text-gray-400" />
            <span className="mt-2 block text-sm font-medium text-gray-900">
              Add Product
            </span>
          </a>
          <a
            href="/dashboard/categories"
            className="relative block rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <TagIcon className="mx-auto h-8 w-8 text-gray-400" />
            <span className="mt-2 block text-sm font-medium text-gray-900">
              Manage Categories
            </span>
          </a>
          <a
            href="/dashboard/reviews"
            className="relative block rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <ChatBubbleLeftRightIcon className="mx-auto h-8 w-8 text-gray-400" />
            <span className="mt-2 block text-sm font-medium text-gray-900">
              View Reviews
            </span>
          </a>
          <a
            href="/dashboard/users"
            className="relative block rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <ChatBubbleLeftRightIcon className="mx-auto h-8 w-8 text-gray-400" />
            <span className="mt-2 block text-sm font-medium text-gray-900">
              Manage Users
            </span>
          </a>
        </div>
      </div>
    </div>
  );
};

export default DashboardOverview;


