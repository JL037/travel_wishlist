export async function fetchTestData(): Promise<any> {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/api/test`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  return response.json();
}
