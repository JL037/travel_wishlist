import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import Navbar from "../components/Navbar";
import "./WishlistPage.css";

export default function WishlistPage() {
  const [wishlist, setWishlist] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [newItemName, setNewItemName] = useState("");
  const [newItemDescription, setNewItemDescription] = useState("");
  const [newItemCity, setNewItemCity] = useState("");
  const [newItemCountry, setNewItemCountry] = useState("");

  // 🟩 Hold the user data
  const [user, setUser] = useState<any>(null);

  // 🟩 Fetch user profile on mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`);
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setUser(data);
      } catch (err) {
        console.error(err);
        alert("Failed to fetch profile. Please refresh!");
      }
    };
    fetchProfile();
  }, []);

  // 🟩 Fetch wishlist on mount
  useEffect(() => {
    fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch wishlist.");
        return res.json();
      })
      .then((data) => setWishlist(data))
      .catch((err) => {
        console.error(err);
        setError("Failed to fetch wishlist.");
      });
  }, []);

  const handleAddWishlistItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: newItemName,
          description: newItemDescription,
          city: newItemCity,
          country: newItemCountry,
        }),
      });
      if (!response.ok) throw new Error("Failed to add wishlist item.");
      const newItem = await response.json();
      setWishlist((prev) => [...prev, newItem]);
      setNewItemName("");
      setNewItemDescription("");
      setNewItemCity("");
      setNewItemCountry("");
    } catch (err) {
      console.error(err);
      alert("Failed to add wishlist item.");
    }
  };

  const handleEdit = async (id: number) => {
    const newName = prompt("Enter new name:");
    const newDescription = prompt("Enter new description:");
    const newVisited = confirm("Mark as visited?");
    if (!newName && !newDescription && !newVisited) {
      alert("No updates made.");
      return;
    }
    const updateData: any = {};
    if (newName) updateData.name = newName;
    if (newDescription) updateData.description = newDescription;
    updateData.visited = newVisited;
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });
      if (!response.ok) throw new Error("Failed to update wishlist item.");
      const updatedItem = await response.json();
      setWishlist((prev) =>
        prev.map((item) => (item.id === id ? updatedItem : item))
      );
    } catch (err) {
      console.error(err);
      alert("Failed to update wishlist item.");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this item?")) return;
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete wishlist item.");
      setWishlist((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete wishlist item.");
    }
  };

  if (error)
    return (
      <p style={{ color: "red", textAlign: "center", marginTop: "2rem" }}>
        {error}
      </p>
    );

  // 🟩 Show loading state for user
  if (user === null) {
    return (
      <p style={{ color: "#aaa", textAlign: "center", marginTop: "2rem" }}>
        Loading user data...
      </p>
    );
  }

  return (
    <div>
      {/* 🟩 Use optional chaining to avoid crash */}
      <Navbar username={user?.username} />

      <div className="wishlist-container">
        <form onSubmit={handleAddWishlistItem} className="wishlist-form">
          <input
            type="text"
            placeholder="Name"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={newItemDescription}
            onChange={(e) => setNewItemDescription(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="City"
            value={newItemCity}
            onChange={(e) => setNewItemCity(e.target.value)}
            required
          />
          <select
            value={newItemCountry}
            onChange={(e) => setNewItemCountry(e.target.value)}
            required
          >
            <option value="">Select a country</option>
            {/* 🟩 Your full country list... */}
            <option value="United States">United States</option>
            <option value="Canada">Canada</option>
            <option value="Mexico">Mexico</option>
            <option value="United Kingdom">United Kingdom</option>
            <option value="France">France</option>
            <option value="Spain">Spain</option>
            <option value="Italy">Italy</option>
            <option value="Germany">Germany</option>
            <option value="Australia">Australia</option>
            <option value="New Zealand">New Zealand</option>
            <option value="Japan">Japan</option>
            <option value="China">China</option>
            <option value="South Korea">South Korea</option>
            <option value="India">India</option>
            <option value="Brazil">Brazil</option>
            <option value="Argentina">Argentina</option>
            <option value="Thailand">Thailand</option>
            <option value="Vietnam">Vietnam</option>
            <option value="South Africa">South Africa</option>
            <option value="Egypt">Egypt</option>
            <option value="Poland">Poland</option>
            <option value="Netherlands">Netherlands</option>
            <option value="Portugal">Portugal</option>
            <option value="Greece">Greece</option>
          </select>

          <button type="submit">Add to Wishlist</button>
        </form>

        <div className="wishlist-items-container">
          {wishlist.length === 0 ? (
            <p>No items in your wishlist yet.</p>
          ) : (
            wishlist.map((item) => (
              <div key={item.id} className="wishlist-item-card">
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <p>
                  {item.city}, {item.country}
                </p>
                <p>Status: {item.visited ? "Visited" : "Not visited"}</p>
                <div className="wishlist-item-actions">
                  <button onClick={() => handleEdit(item.id)}>Edit</button>
                  <button onClick={() => handleDelete(item.id)}>Delete</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
