import { useEffect, useState } from "react";
import { fetchAnalytics } from "../../api/analytics";
import type { AnalyticsData } from "./analyticsTypes";

export default function AnalyticsBoard() {
    const [data, setData] = useState<AnalyticsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchAnalytics()
            .then((res) => setData(res))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);
    
    if (loading) return <p>Loading analytics...</p>;
    if (error) return <p>Error: {error}</p>;
    if (!data) return null;

    return (
        <div className="analytics-board">
            <h2>Your Travel Stats</h2>
            <p>Countries Visited: {data.countries_visited}</p>
            <p>Cities Visited: {data.cities_visited}</p>
            <p>Wishlist Remaining: {data.wishlist_remaining}</p>
            <p>Most Visited Country: {data.most_visited_country}</p>

            <h3>Most Recent Trip</h3>
            {data.most_recent_trip ? (
                <ul>
                    <li>{data.most_recent_trip.city}, {data.most_recent_trip.country}</li>
                    <li>Visited On: {data.most_recent_trip.visited_on}</li>
                    <li>Rating: {data.most_recent_trip.rating ?? "N/A"}</li>
                    <li>Days Since: {data.days_since_last_trip}</li>
                </ul>
            ) : (
                <p>No trips yet</p>
            )}

            <h3>Upcoming Trip</h3>
            {data.nearest_upcoming_trip ? (
                <ul>
                    <li>{data.nearest_upcoming_trip.city}, {data.nearest_upcoming_trip.country}</li>
                    <li>Date: {data.nearest_upcoming_trip.proposed_date}</li>
                </ul>
            ) : (
                <p>No upcoming trip planned</p>
            )}

            <h3>Highest Rated Trip</h3>
            {data.highest_rated_trip ? (
                <ul>
                    <li>{data.highest_rated_trip.city}, {data.highest_rated_trip.country}</li>
                    <li>Rating: {data.highest_rated_trip.rating}</li>
                </ul>
            ): (
                <p>No ratings yet</p>
            )}
        </div>  
    );
}