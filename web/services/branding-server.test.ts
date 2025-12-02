import type { BrandingApiResponse } from "@/types/branding";
import { API_BASE_URL } from "@/config/api";
import { BRANDING_ENDPOINT, DEFAULT_BRANDING } from "@/config/branding";

import { fetchBrandingServer } from "./branding-server";

global.fetch = jest.fn();

const createMockApiResponse = (
  overrides?: Partial<BrandingApiResponse>
): BrandingApiResponse => ({
  application_title: "Server Test App",
  favicon_url: "/server-favicon.ico",
  apple_touch_icon_url: "/server-apple-icon.png",
  manifest_url: "/server-manifest.json",
  environment_suffix: "ServerTest",
  environment: "server-testing",
  version: "2.0.0",
  ...overrides,
});

describe("fetchBrandingServer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (fetch as jest.Mock).mockClear();
  });

  it("fetches branding from API successfully", async () => {
    const mockResponse = createMockApiResponse();
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await fetchBrandingServer();

    expect(fetch).toHaveBeenCalledWith(`${API_BASE_URL}${BRANDING_ENDPOINT}`, {
      cache: "no-store",
    });
    expect(result.branding.applicationTitle).toBe("Server Test App");
    expect(result.environment).toBe("server-testing");
    expect(result.version).toBe("2.0.0");
    expect(result.resolvedFromApi).toBe(true);
  });

  it("falls back to defaults when API returns non-ok status", async () => {
    const consoleSpy = jest.spyOn(console, "error").mockImplementation();
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
    });

    const result = await fetchBrandingServer();

    expect(result.branding).toEqual(DEFAULT_BRANDING);
    expect(result.environment).toBe(process.env.NODE_ENV || "development");
    expect(result.version).toBe("unknown");
    expect(result.resolvedFromApi).toBe(false);

    expect(consoleSpy).toHaveBeenCalledWith(
      "[branding-server] Failed to fetch branding:",
      expect.any(Error)
    );

    consoleSpy.mockRestore();
  });

  it("falls back to defaults when fetch throws error", async () => {
    const consoleSpy = jest.spyOn(console, "error").mockImplementation();
    (fetch as jest.Mock).mockRejectedValueOnce(new Error("Network error"));

    const result = await fetchBrandingServer();

    expect(result.branding).toEqual(DEFAULT_BRANDING);
    expect(result.resolvedFromApi).toBe(false);

    consoleSpy.mockRestore();
  });

  it("handles missing optional fields with defaults", async () => {
    const mockResponse = createMockApiResponse({
      application_title: undefined,
      apple_touch_icon_url: undefined,
      manifest_url: undefined,
    });
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await fetchBrandingServer();

    expect(result.branding.applicationTitle).toBe(
      DEFAULT_BRANDING.applicationTitle
    );
    expect(result.branding.appleTouchIconUrl).toBe(
      DEFAULT_BRANDING.appleTouchIconUrl
    );
    expect(result.branding.manifestUrl).toBe(DEFAULT_BRANDING.manifestUrl);
  });

  it("trims environment suffix", async () => {
    const mockResponse = createMockApiResponse({
      environment_suffix: "  Production  ",
    });
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await fetchBrandingServer();

    expect(result.environmentSuffix).toBe("Production");
  });

  it("treats empty environment suffix as undefined", async () => {
    const mockResponse = createMockApiResponse({
      environment_suffix: "   ",
    });
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await fetchBrandingServer();

    expect(result.environmentSuffix).toBeUndefined();
  });

  it("trims environment and version strings", async () => {
    const mockResponse = createMockApiResponse({
      environment: "  staging  ",
      version: "  1.2.3  ",
    });
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await fetchBrandingServer();

    expect(result.environment).toBe("staging");
    expect(result.version).toBe("1.2.3");
  });

  it("builds correct API URL without trailing slashes", async () => {
    const mockResponse = createMockApiResponse();
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await fetchBrandingServer();

    const expectedUrl = API_BASE_URL.replace(/\/+$/, "") + BRANDING_ENDPOINT;
    expect(fetch).toHaveBeenCalledWith(expectedUrl, expect.any(Object));
  });
});
