import { useBrandingStore } from "@/stores/branding-store";

import type { BrandingApiResponse } from "@/types/branding";
import { DEFAULT_BRANDING } from "@/config/branding";
import { api } from "@/lib/api-client";

import { refreshBranding } from "./branding";

jest.mock("@/lib/api-client");

const resetBrandingStore = () => {
  const {
    setBranding,
    setEnvironmentSuffix,
    setEnvironment,
    setVersion,
    setLoading,
  } = useBrandingStore.getState();
  setBranding({ ...DEFAULT_BRANDING });
  setEnvironmentSuffix(undefined);
  setEnvironment(undefined);
  setVersion(undefined);
  setLoading(true);
};

const createMockApiResponse = (
  overrides?: Partial<BrandingApiResponse>
): BrandingApiResponse => ({
  application_title: "Test App",
  favicon_url: "/test-favicon.ico",
  apple_touch_icon_url: "/test-apple-icon.png",
  manifest_url: "/test-manifest.json",
  environment_suffix: "Test",
  environment: "testing",
  version: "1.0.0",
  ...overrides,
});

describe("refreshBranding", () => {
  beforeEach(() => {
    resetBrandingStore();
    jest.clearAllMocks();
  });

  it("fetches branding from API and updates store", async () => {
    const mockResponse = createMockApiResponse();
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    const state = useBrandingStore.getState();
    expect(state.branding.applicationTitle).toBe("Test App");
    expect(state.branding.faviconUrl).toBe("/test-favicon.ico");
    expect(state.environmentSuffix).toBe("Test");
    expect(state.environment).toBe("testing");
    expect(state.version).toBe("1.0.0");
  });

  it("handles undefined optional fields", async () => {
    const mockResponse = createMockApiResponse({
      apple_touch_icon_url: undefined,
      manifest_url: undefined,
      environment_suffix: undefined,
    });
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    const state = useBrandingStore.getState();
    expect(state.branding.appleTouchIconUrl).toBe(
      DEFAULT_BRANDING.appleTouchIconUrl
    );
    expect(state.branding.manifestUrl).toBe(DEFAULT_BRANDING.manifestUrl);
    expect(state.environmentSuffix).toBeUndefined();
  });

  it("trims environment suffix whitespace", async () => {
    const mockResponse = createMockApiResponse({
      environment_suffix: "  Staging  ",
    });
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    expect(useBrandingStore.getState().environmentSuffix).toBe("Staging");
  });

  it("treats empty environment suffix as undefined", async () => {
    const mockResponse = createMockApiResponse({
      environment_suffix: "   ",
    });
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    expect(useBrandingStore.getState().environmentSuffix).toBeUndefined();
  });

  it("trims environment and version", async () => {
    const mockResponse = createMockApiResponse({
      environment: "  production  ",
      version: "  2.0.0  ",
    });
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    const state = useBrandingStore.getState();
    expect(state.environment).toBe("production");
    expect(state.version).toBe("2.0.0");
  });

  it("throws error when API fails", async () => {
    const error = new Error("Network error");
    (api.get as jest.Mock).mockRejectedValueOnce(error);

    await expect(refreshBranding()).rejects.toThrow("Network error");
  });

  it("logs error to console when API fails", async () => {
    const consoleSpy = jest.spyOn(console, "error").mockImplementation();
    const error = new Error("API error");
    (api.get as jest.Mock).mockRejectedValueOnce(error);

    await expect(refreshBranding()).rejects.toThrow();

    expect(consoleSpy).toHaveBeenCalledWith(
      "[branding] Failed to refresh branding:",
      error
    );

    consoleSpy.mockRestore();
  });

  it("uses cache: no-store for API request", async () => {
    const mockResponse = createMockApiResponse();
    (api.get as jest.Mock).mockResolvedValueOnce(mockResponse);

    await refreshBranding();

    expect(api.get).toHaveBeenCalledWith("/branding", {
      cache: "no-store",
    });
  });
});
