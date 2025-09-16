import { Suspense, lazy, useState} from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { NotificationProvider } from "./context/NotificationContext.jsx";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ErrorMessage from "./components/ErrorMessage";
import ScrollToTop from "./components/ScrollToTop";
import "./App.css";
import ProtectedRoute from "./components/ProtectedRoute"; 

// Lazy load components
const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/Login"));
const Signup = lazy(() => import("./pages/Signup"));
const Profile = lazy(() => import("./pages/Profile"));
const EmailVerification = lazy(() => import("./pages/EmailVerification"));
const SignupSuccess = lazy(() => import("./pages/SignupSuccess"));
const ForgotPassword = lazy(() => import("./pages/ForgotPassword"));
const ResetPassword = lazy(() => import("./pages/ResetPassword"));
const ProductDetails = lazy( () => import("./pages/ProductDetails"));
const OrderHistory = lazy(() => import("./pages/OrderHistory"));
const OrderDetails = lazy(() => import("./pages/OrderDetails"));
const OrderTracking = lazy(() => import("./pages/OrderTracking"));
const Contact = lazy(() => import("./pages/Contact"));
const Cartpage = lazy(() => import("./pages/Cartpage"));
const CheckoutPage = lazy(() => import("./pages/CheckoutPage"));
const PaymentPage = lazy(() => import("./pages/PaymentPage"));
const PaymentSuccessPage = lazy(() => import("./pages/PaymentSuccessPage"));
const NotFound = lazy(() => import("./pages/NotFound"));

// Dashboard components
const DashboardOverview = lazy(() => import("./pages/dashboard/DashboardOverview"));
const ProductsPage = lazy(() => import("./pages/dashboard/ProductsPage"));
const CategoriesPage = lazy(() => import("./pages/dashboard/CategoriesPage"));
const ReviewsPage = lazy(() => import("./pages/dashboard/ReviewsPage"));
const UsersPage = lazy(() => import("./pages/dashboard/UsersPage"));
const DashboardLayout = lazy(() => import("./components/dashboard/DashboardLayout"));
const AdminProtectedRoute = lazy(() => import("./components/AdminProtectedRoute"));

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <AuthProvider>
        <NotificationProvider>
          <div className="min-h-screen flex flex-col">
            <ErrorMessage />
            <Navbar />
            <main className="flex-1">
              <Suspense
                fallback={
                  <div className="min-h-screen flex items-center justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
                  </div>
                }
              >
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/signup" element={<Signup />} />
                  <Route path="/signup-success" element={<SignupSuccess />} />
                  <Route path="/verify-email/:token" element={<EmailVerification />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password/:token" element={<ResetPassword />} />
                  <Route
                    path="/profile"
                    element={
                      <ProtectedRoute>
                        <Profile />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/orders"
                    element={
                      <ProtectedRoute>
                        <OrderHistory />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/orders/:orderId"
                    element={
                      <ProtectedRoute>
                        <OrderDetails />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/cart"
                    element={
                      <ProtectedRoute>
                        <Cartpage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/checkout"
                    element={
                      <ProtectedRoute>
                        <CheckoutPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/payment/:orderId"
                    element={
                      <ProtectedRoute>
                        <PaymentPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/payment-success/:paymentId"
                    element={
                      <ProtectedRoute>
                        <PaymentSuccessPage />
                      </ProtectedRoute>
                    }
                  />
                  <Route path="/product/:id" element={<ProductDetails />} />
                  <Route path="/track" element={<OrderTracking />} />
                  <Route path="/track/:orderNumber" element={<OrderTracking />} />
                  <Route path="/contact" element={<Contact />} />
                  
                  {/* Dashboard Routes */}
                  <Route
                    path="/dashboard"
                    element={
                      <AdminProtectedRoute>
                        <DashboardLayout>
                          <DashboardOverview />
                        </DashboardLayout>
                      </AdminProtectedRoute>
                    }
                  />
                  <Route
                    path="/dashboard/products"
                    element={
                      <AdminProtectedRoute>
                        <DashboardLayout>
                          <ProductsPage />
                        </DashboardLayout>
                      </AdminProtectedRoute>
                    }
                  />
                  <Route
                    path="/dashboard/categories"
                    element={
                      <AdminProtectedRoute>
                        <DashboardLayout>
                          <CategoriesPage />
                        </DashboardLayout>
                      </AdminProtectedRoute>
                    }
                  />
                  <Route
                    path="/dashboard/reviews"
                    element={
                      <AdminProtectedRoute>
                        <DashboardLayout>
                          <ReviewsPage />
                        </DashboardLayout>
                      </AdminProtectedRoute>
                    }
                  />
                  <Route
                    path="/dashboard/users"
                    element={
                      <AdminProtectedRoute>
                        <DashboardLayout>
                          <UsersPage />
                        </DashboardLayout>
                      </AdminProtectedRoute>
                    }
                  />
                  
                  {/* 404 page route */}
                  <Route path="/404" element={<NotFound />} />
                  {/* Catch-all route for 404 */}
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Suspense>
            </main>
            <Footer />
          </div>
        </NotificationProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;