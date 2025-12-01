import { useBrandingStore } from "@/stores/branding-store";

import type { BrandingPayload } from "@/types/branding";
import { DEFAULT_BRANDING } from "@/config/branding";

const cloneDefaultBranding = (): BrandingPayload => ({
  applicationTitle: DEFAULT_BRANDING.applicationTitle,
  faviconUrl: DEFAULT_BRANDING.faviconUrl,
  appleTouchIconUrl: DEFAULT_BRANDING.appleTouchIconUrl,
  manifestUrl: DEFAULT_BRANDING.manifestUrl,
});

describe("branding store", () => {
  beforeEach(() => {
    const { setBranding, setEnvironmentSuffix, setLoading } =
      useBrandingStore.getState();
    setBranding(cloneDefaultBranding());
    setEnvironmentSuffix(undefined);
    setLoading(true);
  });

  it("starts with default payload and loading true", () => {
    const state = useBrandingStore.getState();
    expect(state.branding).toEqual(DEFAULT_BRANDING);
    expect(state.isLoading).toBe(true);
    expect(state.environmentSuffix).toBeUndefined();
  });

  it("updates branding payload immutably", () => {
    const customBranding: BrandingPayload = {
      applicationTitle: "Custom Ops",
      faviconUrl: "/custom.ico",
      appleTouchIconUrl: "/custom-apple.png",
      manifestUrl: "/custom-manifest.json",
    };

    useBrandingStore.getState().setBranding(customBranding);

    const state = useBrandingStore.getState();
    expect(state.branding).toEqual(customBranding);
    expect(state.branding).not.toBe(DEFAULT_BRANDING);
  });

  it("toggles loading flag", () => {
    useBrandingStore.getState().setLoading(false);
    expect(useBrandingStore.getState().isLoading).toBe(false);
    useBrandingStore.getState().setLoading(true);
    expect(useBrandingStore.getState().isLoading).toBe(true);
  });

  it("updates environment suffix and allows clearing", () => {
    useBrandingStore.getState().setEnvironmentSuffix("Preview");
    expect(useBrandingStore.getState().environmentSuffix).toBe("Preview");

    useBrandingStore.getState().setEnvironmentSuffix(undefined);
    expect(useBrandingStore.getState().environmentSuffix).toBeUndefined();
  });
});
