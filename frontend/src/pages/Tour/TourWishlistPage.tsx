import TourNavbar from "../../components/TourNavBar";
import { demoWishlist } from "../../mock/demoData";
import "../WishlistPage.css"; // optional: reuse the styling

export default function TourWishlistPage() {
  const wishlist = demoWishlist;

  const handleAdd = () => {
    alert("To save locations, please create an account!");
  };

  return (
    <>
      <TourNavbar />

      <div className="wishlist-container">
        <h2>Explore Your Wishlist (Tour Mode)</h2>

        <div className="wishlist-list">
          {wishlist.map((item) => (
            <div className="wishlist-item" key={item.id}>
              <h3>{item.city}, {item.country}</h3>
              <p>{item.description}</p>
              {item.visited && <span className="visited-badge">✅ Visited</span>}
            </div>
          ))}
        </div>

        <button className="add-location-btn" onClick={handleAdd}>
          Add New Location
        </button>
      </div>
    </>
  );
}
