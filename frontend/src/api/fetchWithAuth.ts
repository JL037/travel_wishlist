// frontend/src/api/fetchWithAuth.ts
export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const config: RequestInit = {
    ...options,
    credentials: "include",
  };

  let res = await fetch(url, config);

  if (res.status === 401) {

    const refreshRes = await fetch("http://localhost:8000/auth/refresh", {
      method: "POST",
      credentials: "include",
    });

    if (refreshRes.ok) {
      res = await fetch(url, config);
    } else {
      window.location.href = "/";
      return res;
    }
  }

  return res;
}
