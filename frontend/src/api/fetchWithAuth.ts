// frontend/src/api/fetchWithAuth.ts
export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const config: RequestInit = {
    ...options,
    credentials: "include",
  };

  let res = await fetch(url, config);

  if (res.status === 401) {
    // Attempt to refresh token
    const refreshRes = await fetch(`${import.meta.env.VITE_API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (refreshRes.ok) {
      // Try original request again
      res = await fetch(url, config);
    }
    // ⚠️ Do NOT redirect here. Let your app handle it via `useAuthUser`.
    return res;
  }

  return res;
}
