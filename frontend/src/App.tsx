import { BrowserRouter, Routes, Route } from "react-router-dom";
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


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
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


      </Routes>
    </BrowserRouter>
  );
}


  


