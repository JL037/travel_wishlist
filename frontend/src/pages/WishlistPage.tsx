import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function WishlistPage() {
  const [wishlist, setWishlist] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [newItemName, setNewItemName] = useState("");
  const [newItemDescription, setNewItemDescription] = useState("");
  // 🆕 Add state for city and country
  const [newItemCity, setNewItemCity] = useState("");
  const [newItemCountry, setNewItemCountry] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("Not logged in!");
      return;
    }

    fetch("http://localhost:8000/wishlist", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
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
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/wishlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: newItemName,
          description: newItemDescription,
          city: newItemCity,       // 🆕 Add city to payload
          country: newItemCountry, // 🆕 Add country to payload
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add wishlist item.");
      }

      const newItem = await response.json();
      setWishlist((prev) => [...prev, newItem]);
      setNewItemName("");
      setNewItemDescription("");
      // 🆕 Reset city and country fields
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

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      return;
    }

    const updateData: any = {};
    if (newName) updateData.name = newName;
    if (newDescription) updateData.description = newDescription;
    updateData.visited = newVisited;

    try {
      const response = await fetch(`http://localhost:8000/wishlist/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        throw new Error("Failed to update wishlist item.");
      }

      const updatedItem = await response.json();
      setWishlist((prev) =>
        prev.map((item) => (item.id === id ? updatedItem : item))
      );
    } catch (err) {
      console.error(err);
      alert("Failed to update wishlist item.");
    }
    console.log("Updating item with ID:", id, "and data:", updateData);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this item?")) {
      return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/wishlist/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete wishlist item.");
      }

      setWishlist((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete wishlist item.");
    }
  };

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h1>My Wishlist</h1>

      {/* New navigation buttons */}
      <button onClick={() => navigate("/profile")} style={{ marginRight: "0.5rem" }}>
        Go to Profile
      </button>
      <button onClick={() => navigate("/visited")} style={{ marginRight: "0.5rem" }}>
        Go to Visited
      </button>

      <form onSubmit={handleAddWishlistItem}>
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
        {/* 🆕 Add city and country inputs */}
        <input
          type="text"
          placeholder="City"
          value={newItemCity}
          onChange={(e) => setNewItemCity(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Country"
          value={newItemCountry}
          onChange={(e) => setNewItemCountry(e.target.value)}
          required
        />
        <button type="submit">Add to Wishlist</button>
      </form>

      <div>
        {wishlist.map((item) => (
          <div
            key={item.id}
            style={{
              marginBottom: "0.5rem",
              backgroundColor: "#1e1e1e",
              padding: "0.5rem",
              borderRadius: "4px",
              color: "#ffffff",
            }}
          >
            <span>
              {item.name} - {item.description} -{" "}
              {item.visited ? "Visited" : "Not visited"}
            </span>
            <button
              onClick={() => handleEdit(item.id)}
              style={{ marginLeft: "0.5rem" }}
            >
              Edit
            </button>
            <button
              onClick={() => handleDelete(item.id)}
              style={{ marginLeft: "0.5rem" }}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
