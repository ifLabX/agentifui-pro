import {
  API_DEFAULT_CREDENTIALS,
  API_DEFAULT_HEADERS,
  API_REQUEST_TIMEOUT_MS,
  buildApiUrl,
} from "@/config/api";

type Primitive = string | number | boolean;

type QueryValue = Primitive | null | undefined;

export type QueryParams = Record<string, QueryValue | QueryValue[]>;

export interface ApiRequestOptions extends Omit<RequestInit, "body"> {
  query?: QueryParams;
  body?: BodyInit | Record<string, unknown> | null;
  timeoutMs?: number;
  /**
   * Force skipping JSON serialization for plain objects.
   */
  rawBody?: boolean;
}

export class ApiError extends Error {
  status: number;
  statusText: string;
  payload: unknown;

  constructor(response: Response, payload: unknown) {
    super(`Request failed with status ${response.status}`);
    this.name = "ApiError";
    this.status = response.status;
    this.statusText = response.statusText;
    this.payload = payload;
  }
}

const isPlainObject = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const encodeQuery = (query?: QueryParams): string | undefined => {
  if (!query) return undefined;
  const params = new URLSearchParams();

  Object.entries(query).forEach(([key, value]) => {
    if (value === undefined || value === null) return;
    const append = (val: QueryValue) => {
      if (val === undefined || val === null) return;
      params.append(key, String(val));
    };

    if (Array.isArray(value)) {
      value.forEach(append);
    } else {
      append(value);
    }
  });

  const queryString = params.toString();
  return queryString ? `?${queryString}` : undefined;
};

const mergeHeaders = (
  baseHeaders: HeadersInit,
  overrideHeaders?: HeadersInit
): Headers => {
  const headers = new Headers(baseHeaders);
  if (!overrideHeaders) return headers;
  new Headers(overrideHeaders).forEach((value, key) => {
    headers.set(key, value);
  });
  return headers;
};

const createTimeoutController = (
  timeoutMs: number,
  signal?: AbortSignal | null
): AbortController => {
  const controller = new AbortController();

  const timer = setTimeout(() => {
    controller.abort();
  }, timeoutMs);

  if (signal) {
    if (signal.aborted) {
      controller.abort();
    } else {
      signal.addEventListener("abort", () => controller.abort(), {
        once: true,
      });
    }
  }

  controller.signal.addEventListener(
    "abort",
    () => {
      clearTimeout(timer);
    },
    { once: true }
  );

  return controller;
};

const resolveBody = (
  body: ApiRequestOptions["body"],
  headers: Headers,
  rawBody?: boolean
): BodyInit | undefined => {
  if (body === undefined || body === null) return undefined;

  if (rawBody) return body as BodyInit;

  if (
    body instanceof Blob ||
    body instanceof FormData ||
    body instanceof URLSearchParams ||
    typeof body === "string"
  ) {
    return body;
  }

  if (isPlainObject(body)) {
    if (!headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    return JSON.stringify(body);
  }

  return body as BodyInit;
};

export const apiRequest = async <T = unknown>(
  path: string,
  {
    method = "GET",
    query,
    body,
    headers: overrideHeaders,
    timeoutMs = API_REQUEST_TIMEOUT_MS,
    signal,
    rawBody = false,
    credentials = API_DEFAULT_CREDENTIALS,
    ...rest
  }: ApiRequestOptions = {}
): Promise<T> => {
  const url = new URL(buildApiUrl(path));
  const queryString = encodeQuery(query);
  if (queryString) {
    url.search = queryString.slice(1);
  }

  const headers = mergeHeaders(API_DEFAULT_HEADERS, overrideHeaders);

  const controller = createTimeoutController(timeoutMs, signal);

  const resolvedBody = resolveBody(body, headers, rawBody);

  const response = await fetch(url.toString(), {
    method,
    headers,
    credentials,
    body: resolvedBody,
    signal: controller.signal,
    ...rest,
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const contentType = response.headers.get("Content-Type") ?? "";

  const parseResponse = async (): Promise<unknown> => {
    if (contentType.includes("application/json")) {
      return response.json();
    }
    if (contentType.includes("text/")) {
      return response.text();
    }
    return response.arrayBuffer();
  };

  const payload = await parseResponse();

  if (!response.ok) {
    throw new ApiError(response, payload);
  }

  return payload as T;
};
