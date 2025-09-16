import axios from 'axios';

// Determine the base URL based on environment
const getBaseURL = () => {
  // For production (GitHub Pages), use ngrok URL
  if (window.location.hostname === 'marzok16.github.io') {
    return 'https://99e4adbd0611.ngrok-free.app/api';
  }
  // For LocalTunnel frontend, use ngrok backend
  if (window.location.hostname.includes('loca.lt')) {
    return 'https://99e4adbd0611.ngrok-free.app/api';
  }
  // For ngrok frontend, also use ngrok backend
  if (window.location.hostname.includes('ngrok-free.app')) {
    return 'https://99e4adbd0611.ngrok-free.app/api';
  }
  // For local development
  return 'http://127.0.0.1:8000/api';
};

const BASE_URL = getBaseURL();

const instance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
    }
});

// Add request interceptor to attach JWT token and ngrok bypass header
instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        
        // Always add ngrok bypass header for ngrok URLs
        if (BASE_URL.includes('ngrok-free.app')) {
            config.headers['ngrok-skip-browser-warning'] = 'true';
        }
        
        // Don't add token for login, signup, and public endpoints
        const publicPaths = [
            '/users/login/',
            '/users/signup/',
            '/payments/stripe-config/',
            '/users/verify-email/',
            '/users/resend-verification/',
            '/users/forgot-password/',
            '/users/reset-password/'
        ];
        const isPublicPath = publicPaths.some(path => config.url?.includes(path));
        if (token && !isPublicPath) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add response interceptor for debugging
instance.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('Server Error:', {
            status: error.response?.status,
            data: error.response?.data,
            url: error.config?.url
        });
        return Promise.reject(error);
    }
);

export default instance;
