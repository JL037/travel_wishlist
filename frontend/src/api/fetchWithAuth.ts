// frontend/src/api/fetchWithAuth.ts
export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const config: RequestInit = {
    ...options,
    credentials: "include",
  };

  let res = await fetch(url, config);

  if (res.status === 401) {
    console.warn("Access token expired, trying refresh...");

    const refreshRes = await fetch("http://localhost:8000/auth/refresh", {
      method: "POST",
      credentials: "include",
    });

    if (refreshRes.ok) {
      console.log("✅ Refresh worked, retrying original request...");
      res = await fetch(url, config);
    } else {
      console.warn("❌ Refresh failed, redirecting to login");
      window.location.href = "/";
      return res;
    }
  }

  return res;
}
