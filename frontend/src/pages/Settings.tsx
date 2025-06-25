import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import Navbar from "../components/Navbar";
import "./Settings.css";
import useAuthUser from "../hooks/useAuthUser";

export default function SettingsPage() {
  const { user, loading } = useAuthUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  //  Fetch user on mount
  useEffect(() => {
    if (user) {
      setUsername(user.username || "");
      setEmail(user.email || "");
    }
  }, [user]);

  //  Handle profile update
  const handleProfileUpdate = async () => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`, {
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

  //  Handle password change
  const handleChangePassword = async () => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/change-password`, {
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
    if (!confirm(
        "Are you sure you want to delete your account? This action is permanent."
    )) return;

    try{
        const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/delete-account`, {
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

  if (loading) {
    return <p style={{ textAlign: "center", marginTop: "2rem", color: "#999"}}>Loading profile...</p>;
  }

  if (!user) {
    window.location.href = "/login";
    return null;
  }

  // ✅ Page content
return (
  <>
    <Navbar username={user.username} />

    <div className="settings-container">
      <h2>Settings</h2>

      <section>
        <h3>Update Profile</h3>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <button onClick={handleProfileUpdate} className="update-btn">
          Update Profile
        </button>
      </section>

      <section>
        <h3>Change Password</h3>
        <label htmlFor="current-password">Current Password</label>
        <input
          id="current-password"
          type="password"
          placeholder="Current Password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />

        <label htmlFor="new-password">New Password</label>
        <input
          id="new-password"
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />

        <button onClick={handleChangePassword} className="update-btn">
          Change Password
        </button>
      </section>

      <section>
        <h3 style={{ color: "red" }}>Area 51</h3>
        <button onClick={handleDeleteAccount} className="delete-btn">
          Delete My Account
        </button>
      </section>
    </div>
  </>
);
}
