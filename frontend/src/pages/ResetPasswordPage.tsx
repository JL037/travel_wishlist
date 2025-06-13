import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import "./ForgotPasswordPage.css"


export default function ResetPasswordPage () {
    const [searchParams] = useSearchParams();
    const [newPassword, setNewPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const token = searchParams.get("token");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage("");
        setError("");

        try {
            const res = await fetch("https://api.travelwishlist.app/auth/reset-password", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    token,
                    new_password: newPassword,
                }),
            });
            const data = await res.json();

            if (res.ok) {
                setMessage("Password reset successfully! You can now log in.")
                setTimeout(() => navigate("/"), 3000);
            }   else {
                setError(data.detail || "Something went wrong.");
            }
        }   catch (err) {
            setError("Server error. Please try again");
        }   finally {
            setIsLoading(false);
        }
    };

    if (!token) {
        return <p className="error">Invalid or missing token.</p>;
    }

    return (
        <div className="forgot-password-container">
            <h2>Reset Your Password</h2>
            <form onSubmit={handleSubmit}>
                <label>New Password</label>
                <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? "Resetting..." : "Reset Password"}
                </button>
            </form>
            {message && <p className="success">{message}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
}