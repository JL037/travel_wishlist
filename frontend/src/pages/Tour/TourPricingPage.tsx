import { useState } from "react";
import "../PricingPage.css"; // Reuse the main styles
import TourNavBar from "../../components/TourNavBar"; // Use the tour-safe nav

export default function TourPricingPage() {
  const [thankYou, setThankYou] = useState(false);

  const handleClick = () => {
    setThankYou(true);
  };

  return (
    <div>
      <TourNavBar />

      <div className="pricing-header-box">
        <div className="pricing-container">
          <h1 className="pricing-title">Pricing</h1>
          <p className="pricing-subtitle">
            Let’s keep it simple and fun! No payments here—just support me and this project.
          </p>
        </div>

        <div className="tier" onClick={handleClick}>
          <h2>Free Tier</h2>
          <p>Use the app and enjoy—no strings attached.</p>
        </div>

        <div className="tier" onClick={handleClick}>
          <h2>Pro Tier</h2>
          <p>Share this with your friends or post about it on social media!</p>
        </div>

        <div className="tier" onClick={handleClick}>
          <h2>Premium Tier</h2>
          <p>Hire me! Let’s collaborate and build cool things together.</p>
        </div>

        {thankYou && (
          <div className="thank-you">
            <h1>Thank you for sharing!</h1>
          </div>
        )}
      </div>
    </div>
  );
}
