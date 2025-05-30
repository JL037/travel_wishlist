import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import ProfilePage from "./pages/ProfilePage";
import WishlistPage from "./pages/WishlistPage";
import WishlistItemPage from "./pages/WishlistItemPage";
import VisitedLocationsPage from "./pages/VisitedLocationsPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/wishlist" element={<WishlistPage />} />
        <Route path="/wishlist/:id" element={<WishlistItemPage />} />
        <Route path="/visited" element={<VisitedLocationsPage />} />

      </Routes>
    </BrowserRouter>
  );
}


  


