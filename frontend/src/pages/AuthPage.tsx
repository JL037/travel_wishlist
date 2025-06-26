import { useState } from "react";
import {FaEye, FaEyeSlash} from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import "./AuthPage.css";

export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const url = isLogin
      ? `${import.meta.env.VITE_API_URL}/auth/login`
      : `${import.meta.env.VITE_API_URL}/auth/register`;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: isLogin
          ? JSON.stringify({ email, password })
          : JSON.stringify({ email, username, password }),
      });

      if (!response.ok) {
        throw new Error(isLogin ? "Login failed!" : "Registration failed!");
      }

      if (isLogin) {
        navigate("/profile");
      } else {
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
    <div id="auth-page" className="login-container">
      <div className="login-box">
        <img src="/globe.jpg" alt="Globe" className="globe-icon" />
        <h1>{isLogin ? "Welcome back, Explorer!" : "Create your account"}</h1>
        <p>
          {isLogin
            ? "Log in to continue your travel dreams 🌍"
            : "Join us and start your journey 🌟"}
        </p>

        <form onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          {!isLogin && (
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        )}
          <div className="password-wrapper">
         <input
          type={showPassword ? "text" : "password"}
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="password-input"
          />
         <span
          className="eye-toggle" onClick={() => setShowPassword((prev) => !prev)}
          style={{
          position: "absolute",
          right: "10px",
          top: "50%",
          transform: "translateY(-50%)",
          cursor: "pointer",
          color: "#888",
          fontSize: "1.1rem",
          display: "flex",
          alignItems: "center",
          height: "100%"
        }}
          >
          {showPassword ? <FaEyeSlash /> : <FaEye />}
         </span>
          </div>
          <button type="submit">{isLogin ? "Login" : "Register"}</button>
        
          <p className="forgot-link">
            <a href="/forgot-password">Forgot Password?</a>
          </p>
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

        <img
          src="/logo.png"
          alt="TWL Logo"
          style={{
            width: "100px",
            marginTop: "10px",
            opacity: 0.7,
            filter: "invert(1)",
          }}
        />

        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
}
