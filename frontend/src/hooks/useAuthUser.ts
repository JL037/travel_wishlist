import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";

export default function useAuthUser() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`);
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setUser(data);
      } catch {
        setUser(null);  // if error, set null
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  return { user, loading };
}
