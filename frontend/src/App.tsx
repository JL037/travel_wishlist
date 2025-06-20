import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import ProfilePage from "./pages/ProfilePage";
import WishlistPage from "./pages/WishlistPage";
import WishlistItemPage from "./pages/WishlistItemPage";
import VisitedLocationsPage from "./pages/VisitedLocationsPage";
import TestCalendar from "./components/TestCalendar";
import PricingPage from "./pages/PricingPage";
import FAQPage from "./pages/FAQPage";
import SettingsPage from "./pages/Settings";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import TourWishlistPage from "./pages/Tour/TourWishlistPage";
import TourProfilePage from "./pages/Tour/TourProfilePage";
import TourVisitedLocationsPage from "./pages/Tour/TourVisitedLocationsPage";
import TourFAQPage from "./pages/Tour/TourFAQPage";
import TourPricingPage from "./pages/Tour/TourPricingPage";
import CombinedLocationsPage from "./pages/CombinedLocationsPage";
import useAuthUser from "./hooks/useAuthUser";

// 🔁 This wrapper allows us to use `useLocation` outside the Router
function AppWrapper() {
  const { user, loading } = useAuthUser();
  const location = useLocation();

  // 🔄 Prevent redirect loop by only triggering on root path
  if (loading) return <div>Loading...</div>;
  if (location.pathname === "/") {
    return <Navigate to={user ? "/profile" : "/tour/profile"} replace />;
  }

  return (
    <Routes>
      <Route path="/login" element={<AuthPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/wishlist" element={<WishlistPage />} />
      <Route path="/wishlist/:id" element={<WishlistItemPage />} />
      <Route path="/visited" element={<VisitedLocationsPage />} />
      <Route path="/test-calendar" element={<TestCalendar />} />
      <Route path="/pricing" element={<PricingPage />} />
      <Route path="/faq" element={<FAQPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route path="/tour/wishlist" element={<TourWishlistPage />} />
      <Route path="/tour/profile" element={<TourProfilePage />} />
      <Route path="/tour/visited" element={<TourVisitedLocationsPage />} />
      <Route path="/tour/faq" element={<TourFAQPage />} />
      <Route path="/tour/pricing" element={<TourPricingPage />} />
      <Route path="/all-locations" element={<CombinedLocationsPage />} />  
      
      {/* Redirect to profile if user is logged in, otherwise to tour profile */}


      <Route path="*" element={<h1>404 Not Found</h1>} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  );
}


