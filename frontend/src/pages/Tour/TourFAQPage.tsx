import TourNavBar from "../../components/TourNavBar";
import "../FAQPage.css"; // Reuse the existing styles

export default function TourFAQPage() {
  return (
    <div>
      <TourNavBar />
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
