import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./AuthPage.css"; // Make sure you have this file

export default function AuthPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      });

      if (!response.ok) throw new Error("Login failed!");
      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);
      navigate("/profile");
    } catch (err) {
      console.error(err);
      setError("Login failed. Please check your credentials.");
    }
  };

  return (
  <div className="login-container">
    <div className="login-box">
      <img src="/globe.jpg" alt="Globe" className="globe-icon" />
      <h1>Welcome back, Explorer!</h1>
      <p>Log in to continue your travel dreams 🌍</p>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  </div>
);
}