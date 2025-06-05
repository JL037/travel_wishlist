import Navbar from "../components/Navbar";
import "./FAQPage.css"; // We'll create this next!
import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
export default function FAQPage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetchWithAuth("http://localhost:8000/auth/me");
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


  return (
    <div>
      <Navbar username={user?.username} /> {/* Include the Navbar at the top! */}
      <div className="faq-container">
        <h1 className="faq-title">Frequently Asked Questions</h1>
        <div className="faq-list">
          <div className="faq-item">
            <h3>Q: What is this project all about?</h3>
            <p>
              A: It’s a travel app where you can track your wishlist and visited locations, and even check the weather for your future trips.
            </p>
          </div>
          <div className="faq-item">
            <h3>Q: Is there any cost?</h3>
            <p>
              A: Nope! It’s totally free – just share the app and let people know about it!
            </p>
          </div>
          <div className="faq-item">
            <h3>Q: How can I support you?</h3>
            <p>
              A: You can help by sharing it, using it, and telling your friends. Or check out the Pricing page for other ways to help!
            </p>
          </div>
          <div className="faq-item">
            <h3>Q: Can I suggest features?</h3>
            <p>
              A: Absolutely! Just reach out and let me know what you think would make it even better.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
