import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./AuthPage.css";

export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const url = isLogin
      ? "http://localhost:8000/auth/login"
      : "http://localhost:8000/auth/register";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: isLogin
          ? JSON.stringify({ username, password })
          : JSON.stringify({ email, username, password }),
      });

      if (!response.ok) {
        throw new Error(isLogin ? "Login failed!" : "Registration failed!");
      }

      const data = await response.json();

      if (isLogin) {
        localStorage.setItem("access_token", data.access_token);
        navigate("/profile");
      } else {
        // Registration was successful, switch to login
        setIsLogin(true);
        setEmail("");
        setUsername("");
        setPassword("");
      }

      setError("");
    } catch (err) {
      console.error(err);
      setError(
        isLogin
          ? "Login failed. Please check your credentials."
          : "Registration failed. Please try again."
      );
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <img src="/globe.jpg" alt="Globe" className="globe-icon" />
        <h1>{isLogin ? "Welcome back, Explorer!" : "Create your account"}</h1>
        <p>
          {isLogin
            ? "Log in to continue your travel dreams 🌍"
            : "Join us and start your journey 🌟"}
        </p>

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          )}
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
          <button type="submit">{isLogin ? "Login" : "Register"}</button>
        </form>

        <p>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            style={{
              background: "none",
              border: "none",
              color: "blue",
              cursor: "pointer",
            }}
          >
            {isLogin ? "Register here" : "Login here"}
          </button>
        </p>

        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
}
