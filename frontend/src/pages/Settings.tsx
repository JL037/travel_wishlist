import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import Navbar from "../components/Navbar";
import "./Settings.css";

export default function SettingsPage() {
  const [user, setUser] = useState<any>(null);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  // ✅ Fetch user on mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`);
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setUser(data);
        setUsername(data.username || "");
        setEmail(data.email || "");
      } catch (err) {
        console.error(err);
        alert("Failed to fetch user profile");
      }
    };
    fetchProfile();
  }, []);

  // ✅ Handle profile update
  const handleProfileUpdate = async () => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/me`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Profile update failed");
      alert("Profile updated successfully!");
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ✅ Handle password change
  const handleChangePassword = async () => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/change-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Password change failed");
      alert("Password changed successfully!");
      setCurrentPassword("");
      setNewPassword("");
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDeleteAccount = async () => {
    const confirmed = confirm(
        "Are you sure you want to delete your account? This action is permanent."
    );
    if (!confirmed) return;

    try{
        const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/delete-account`, {
            method: "DELETE",
        });
        
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to delete account");
        alert(data.message);
        window.location.href = "/";
      } catch(err: any) {
        alert(err.message || "Something went wrong");
      }
  };

  // 🟨 Optional loading state
  if (user === null) {
    return (
      <p style={{ textAlign: "center", marginTop: "2rem", color: "#999" }}>
        Loading profile...
      </p>
    );
  }

  // ✅ Page content
  return (
    <>
      <Navbar username={user?.username} />

      <div className="settings-container">
        <h2>Settings</h2>

        <section>
          <h3>Update Profile</h3>
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={handleProfileUpdate}>Update Profile</button>
        </section>

        <section>
          <h3>Change Password</h3>
          <input
            type="password"
            placeholder="Current Password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button onClick={handleChangePassword}>Change Password</button>
        </section>
        <section style={{ borderTop: "1px solid #ccc", marginTop: "2rem", paddingTop: "1rem" }}>
        <h3 style={{ color: "red" }}>Area 51 </h3>
        <button
            onClick={handleDeleteAccount}
            style={{
            backgroundColor: "red",
            color: "white",
            padding: "0.75rem 1rem",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            marginTop: "0.5rem",
        }}
        >
        Delete My Account
        </button>
        </section>
      </div>
    </>
  );
}
