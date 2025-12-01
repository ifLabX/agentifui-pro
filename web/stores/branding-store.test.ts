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
    const {
      setBranding,
      setEnvironmentSuffix,
      setLoading,
      setEnvironment,
      setVersion,
    } = useBrandingStore.getState();
    setBranding(cloneDefaultBranding());
    setEnvironmentSuffix(undefined);
    setEnvironment(undefined);
    setVersion(undefined);
    setLoading(true);
  });

  it("starts with default payload and loading true", () => {
    const state = useBrandingStore.getState();
    expect(state.branding).toEqual(DEFAULT_BRANDING);
    expect(state.isLoading).toBe(true);
    expect(state.environmentSuffix).toBeUndefined();
    expect(state.environment).toBeUndefined();
    expect(state.version).toBeUndefined();
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

  it("stores environment and version", () => {
    useBrandingStore.getState().setEnvironment("staging");
    useBrandingStore.getState().setVersion("1.2.3");

    expect(useBrandingStore.getState().environment).toBe("staging");
    expect(useBrandingStore.getState().version).toBe("1.2.3");

    useBrandingStore.getState().setEnvironment(undefined);
    useBrandingStore.getState().setVersion(undefined);

    expect(useBrandingStore.getState().environment).toBeUndefined();
    expect(useBrandingStore.getState().version).toBeUndefined();
  });
});
