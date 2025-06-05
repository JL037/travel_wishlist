import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import { Calendar, momentLocalizer } from "react-big-calendar";
import type { SlotInfo } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import moment from "moment";
import "./TravelPlanner.css";

const localizer = momentLocalizer(moment);

interface CalendarEvent {
  id: number;
  start: Date;
  end: Date;
  title: string;
  allDay?: boolean;
}

interface NewTravelPlan {
  start_date: Date;
  end_date: Date;
  location: string;
  notes: string;
}

export default function TravelPlanner() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  const fetchEvents = async () => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/travel-plans`);
      if (!res.ok) throw new Error("Failed to load travel plans");
      const data = await res.json();

      const fetchedEvents = data.map((plan: any) => {
        const start = new Date(plan.start_date);
        const end = new Date(plan.end_date);

        if (start.getHours() === 0 && start.getMinutes() === 0) start.setHours(9);
        if (end.getHours() === 0 && end.getMinutes() === 0) end.setHours(17);

        return {
          id: plan.id,
          title: plan.location || "Untitled Trip",
          start,
          end,
          allDay: false,
        };
      });
      setEvents(fetchedEvents);
    } catch (err) {
      console.error("Error fetching travel plans:", err);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleSelectSlot = async (slotInfo: SlotInfo) => {
    const location = prompt("Enter trip location:", "Unknown");
    const notes = prompt("Any notes for this trip?", "");

    const startDate = new Date(slotInfo.start);
    if (startDate.getHours() === 0 && startDate.getMinutes() === 0) startDate.setHours(9);

    const endDate = new Date(slotInfo.end);
    if (endDate.getHours() === 0 && endDate.getMinutes() === 0) endDate.setHours(17);

    const newEvent: NewTravelPlan = {
      start_date: startDate,
      end_date: endDate,
      location: location || "Unknown",
      notes: notes || "",
    };

    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/travel-plans`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newEvent),
      });

      if (!res.ok) {
        const errMessage = await res.text();
        throw new Error(`Failed to save new trip: ${errMessage}`);
      }

      await fetchEvents();
    } catch (err) {
      console.error("Error saving new trip:", err);
      alert("Failed to save your trip. Please try again!");
    }
  };

  const deleteEvent = async (planId: number) => {
    try {
      const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/travel-plans/${planId}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        const errMessage = await res.text();
        throw new Error(`Failed to delete: ${errMessage}`);
      }

      await fetchEvents();
    } catch (err) {
      console.error("Error deleting event:", err);
      alert("Failed to delete the event. Please try again!");
    }
  };

  const handleSelectEvent = (event: CalendarEvent) => {
    const confirmed = window.confirm(`Delete trip to "${event.title}"?`);
    if (confirmed) {
      deleteEvent(event.id);
    }
  };

  return (
    <div>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        selectable
        onSelectSlot={handleSelectSlot}
        onSelectEvent={handleSelectEvent}
        views={["month", "agenda"]}
        defaultView="month"
        toolbar={true}
        style={{ height: 600 }}
      />
    </div>
  );
}

