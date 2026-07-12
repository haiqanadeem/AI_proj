export class ApiError extends Error {
  constructor(public status: number, public message: string, public data?: any) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const url = `${baseUrl}${endpoint}`;

  const headers = new Headers(options.headers || {});
  
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    if (typeof options.body === "string" && options.body.includes("grant_type=")) {
        headers.set("Content-Type", "application/x-www-form-urlencoded");
    } else if (typeof options.body === "string") {
        headers.set("Content-Type", "application/json");
    }
  }

  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }

  let attempt = 0;
  const maxAttempts = 2;

  while (attempt < maxAttempts) {
    try {
      const response = await fetch(url, { ...options, headers });

      if (response.status === 401) {
        if (typeof window !== "undefined" && window.location.pathname !== "/login" && window.location.pathname !== "/register") {
          localStorage.removeItem("token");
          window.location.href = `/login?returnTo=${encodeURIComponent(window.location.pathname)}`;
        }
        throw new ApiError(401, "Unauthorized");
      }

      if (response.status === 422) {
        const data = await response.json().catch(() => ({}));
        throw new ApiError(422, "Validation Error", data.detail);
      }

      if ((response.status === 429 || response.status === 503) && attempt === 0) {
        attempt++;
        await new Promise((resolve) => setTimeout(resolve, 1500));
        continue;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new ApiError(response.status, errorData?.detail || "An error occurred", errorData);
      }

      const text = await response.text();
      return text ? JSON.parse(text) : ({} as T);
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError(500, error instanceof Error ? error.message : "Network Error");
    }
  }
  
  throw new ApiError(500, "Maximum retries exceeded");
}
