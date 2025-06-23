import { useEffect, useState } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import "./TravelPlanner.css"; // ✅ reuse your real styling

const localizer = momentLocalizer(moment);

interface TourPlan {
  location: string;
  start_date: string; // string to keep props easy
  end_date: string;
  notes: string;
}

interface CalendarEvent {
  id: number;
  start: Date;
  end: Date;
  title: string;
  allDay?: boolean;
}

type TourTravelPlannerProps = {
  mockPlans: TourPlan[];
};

export default function TourTravelPlanner({ mockPlans }: TourTravelPlannerProps) {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    const formatted = mockPlans.map((plan, index) => {
      const start = new Date(plan.start_date);
      const end = new Date(plan.end_date);

      // Just like your real version — set default times
      if (start.getHours() === 0) start.setHours(9);
      if (end.getHours() === 0) end.setHours(17);

      return {
        id: index,
        title: plan.location,
        start,
        end,
        allDay: false,
      };
    });

    setEvents(formatted);
  }, [mockPlans]);

  return (
    <div>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        selectable={false}
        views={["month", "agenda"]}
        defaultView="month"
        toolbar={true}
        style={{ height: 600 }}
      />
    </div>
  );
}

