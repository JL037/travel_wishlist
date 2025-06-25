import { useState } from "react";
import "./LocationDetailsModal.css";

type Location = {
  id: number;
  city?: string;
  country?: string;
  notes?: string;
  proposed_date?: string;
  visited_on?: string;
  type: "wishlist" | "visited";
};

type Props = {
  location: Location;
  onClose: () => void;
  onSave: (id: number, data: Partial<Location>) => void;
};

export default function LocationDetailsModal({ location, onClose, onSave }: Props) {
  const [notes, setNotes] = useState(location.notes || "");
  const [date, setDate] = useState(location.proposed_date || location.visited_on || "");

  const handleSave = () => {
    const dataToSend: Partial<Location> = {
      notes: notes || undefined,
      ...(location.type === "wishlist"
        ? { proposed_date: date || undefined }
        : { visited_on: date || undefined }),
    };
    onSave(location.id, dataToSend);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{location.city}, {location.country}</h2>

        <label>Notes:</label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Enter notes about this location..."
        />

        <label>{location.type === "wishlist" ? "Proposed Date:" : "Visited Date:"}</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />

        <div className="modal-actions">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}
