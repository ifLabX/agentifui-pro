import { useBrandingStore } from "@/stores/branding-store";
import { render, waitFor } from "@testing-library/react";

import type { BrandingResult } from "@/types/branding";
import { DEFAULT_BRANDING } from "@/config/branding";

import { BrandingProvider } from "./branding-provider";

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

const createMockBrandingResult = (
  overrides?: Partial<BrandingResult>
): BrandingResult => ({
  branding: {
    applicationTitle: "Test App",
    faviconUrl: "/test-favicon.ico",
    appleTouchIconUrl: "/test-apple-icon.png",
    manifestUrl: "/test-manifest.json",
  },
  environmentSuffix: "Test",
  environment: "testing",
  version: "1.0.0",
  resolvedFromApi: true,
  ...overrides,
});

describe("BrandingProvider", () => {
  beforeEach(() => {
    resetBrandingStore();
  });

  it("syncs initialBranding to store on mount", async () => {
    const mockBranding = createMockBrandingResult();

    render(
      <BrandingProvider initialBranding={mockBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      const state = useBrandingStore.getState();
      expect(state.branding).toEqual(mockBranding.branding);
      expect(state.environmentSuffix).toBe("Test");
      expect(state.environment).toBe("testing");
      expect(state.version).toBe("1.0.0");
      expect(state.isLoading).toBe(false);
    });
  });

  it("updates store when initialBranding prop changes", async () => {
    const initialBranding = createMockBrandingResult({
      branding: {
        applicationTitle: "Initial App",
        faviconUrl: "/initial.ico",
      },
      environment: "staging",
      version: "1.0.0",
    });

    const { rerender } = render(
      <BrandingProvider initialBranding={initialBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      expect(useBrandingStore.getState().branding.applicationTitle).toBe(
        "Initial App"
      );
    });

    const updatedBranding = createMockBrandingResult({
      branding: {
        applicationTitle: "Updated App",
        faviconUrl: "/updated.ico",
      },
      environment: "production",
      version: "2.0.0",
    });

    rerender(
      <BrandingProvider initialBranding={updatedBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      const state = useBrandingStore.getState();
      expect(state.branding.applicationTitle).toBe("Updated App");
      expect(state.environment).toBe("production");
      expect(state.version).toBe("2.0.0");
    });
  });

  it("handles branding without API resolution", async () => {
    const mockBranding = createMockBrandingResult({
      resolvedFromApi: false,
    });

    render(
      <BrandingProvider initialBranding={mockBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      const state = useBrandingStore.getState();
      expect(state.branding).toEqual(mockBranding.branding);
      expect(state.environmentSuffix).toBeUndefined();
      expect(state.environment).toBeUndefined();
      expect(state.version).toBeUndefined();
      expect(state.isLoading).toBe(false);
    });
  });

  it("sets loading to false regardless of API resolution", async () => {
    const mockBranding = createMockBrandingResult({
      resolvedFromApi: false,
    });

    render(
      <BrandingProvider initialBranding={mockBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      expect(useBrandingStore.getState().isLoading).toBe(false);
    });
  });

  it("handles undefined environment suffix gracefully", async () => {
    const mockBranding = createMockBrandingResult({
      environmentSuffix: undefined,
    });

    render(
      <BrandingProvider initialBranding={mockBranding}>
        <div>Test Child</div>
      </BrandingProvider>
    );

    await waitFor(() => {
      expect(useBrandingStore.getState().environmentSuffix).toBeUndefined();
    });
  });

  it("renders children correctly", () => {
    const mockBranding = createMockBrandingResult();

    const { getByText } = render(
      <BrandingProvider initialBranding={mockBranding}>
        <div>Test Child Content</div>
      </BrandingProvider>
    );

    expect(getByText("Test Child Content")).toBeInTheDocument();
  });
});
