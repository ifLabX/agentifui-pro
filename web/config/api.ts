const sanitizeBaseUrl = (value?: string | null): string => {
  if (!value) return "";
  const trimmed = value.trim();
  if (!trimmed) return "";
  return trimmed.replace(/\/+$/, "");
};

const FALLBACK_BASE_URL = "http://localhost:8000";

const rawBaseUrl = sanitizeBaseUrl(process.env.NEXT_PUBLIC_API_URL);

export const API_BASE_URL = rawBaseUrl || FALLBACK_BASE_URL;

const rawTimeout = Number.parseInt(
  process.env.NEXT_PUBLIC_API_TIMEOUT_MS ?? "",
  10
);

export const API_REQUEST_TIMEOUT_MS =
  Number.isFinite(rawTimeout) && rawTimeout > 0 ? rawTimeout : 15000;

export const API_DEFAULT_CREDENTIALS: RequestCredentials = "include";

export const API_DEFAULT_HEADERS: HeadersInit = {
  Accept: "application/json",
};

const ensureAbsolute = (path: string, base: string): string => {
  return new URL(path, base).toString();
};

export const buildApiUrl = (path: string): string => {
  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  if (path.startsWith("/")) {
    const runtimeOrigin =
      typeof window !== "undefined" && window.location
        ? window.location.origin
        : API_BASE_URL;
    return ensureAbsolute(path, runtimeOrigin);
  }

  return `${API_BASE_URL}/${path}`;
};
