export interface RecentTrip {
    name: string | null;
    city: string | null;
    country: string | null;
    visited_on: string | null;
    rating: number | null;
}

export interface UpcomingTrip {
    name: string | null;
    city: string;
    country: string;
    proposed_date: string | null;
    notes?: string | null;
}

export interface HighestRatedTrip {
    name: string | null;
    city: string;
    country: string;
    rating: number | null;
}

export interface AnalyticsData {
    countries_visited: number;
    cities_visited: number;
    wishlist_remaining: number;
    most_visited_country: string | null;
    highest_rated_trip: HighestRatedTrip | null;
    most_recent_trip: RecentTrip | null;
    nearest_upcoming_trip: UpcomingTrip | null;
    days_since_last_trip: number | null;
}

