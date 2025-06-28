import type { AnalyticsData }  from "../components/AnalyticsBoard/analyticsTypes";
import { fetchWithAuth } from "./fetchWithAuth";

export async function fetchAnalytics(): Promise<AnalyticsData> {
    const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/analytics/me`);
    if (!response.ok) throw new Error("Failed to fetch analytics");
    return response.json();
}