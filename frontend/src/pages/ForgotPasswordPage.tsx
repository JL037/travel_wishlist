import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
import "./ForgotPasswordPage.css";

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    // const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage("");
        setError("");

        try{
            const response = await fetch("https://api.travelwishlist.app/auth/forgot-password", {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(email),
            });
            const data = await response.json();
            if (response.ok) {
                setMessage("If your email exists in our system, a reset link was sent.");
                console.log("Token (for dev):", data.reset_token);
            }   else {
                setError(data.detail || "Something went wrong.");
            }
        }   catch (err) {
            setError("Server error. Please try again.");
        }   finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="forgot-password-container">
            <h2>Forgot Your Password</h2>
            <form onSubmit={handleSubmit}>
                <label>Email Address</label>
                <input 
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? "Sending..." : "Send Reset Link"}
                </button>
            </form>
            {message && <p className="success">{message}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );

}