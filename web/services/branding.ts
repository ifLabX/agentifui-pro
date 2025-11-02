import type {
  BrandingApiResponse,
  BrandingPayload,
  BrandingResult,
} from "@/types/branding";
import { BRANDING_ENDPOINT, DEFAULT_BRANDING } from "@/config/branding";

const normalisePayload = (payload: BrandingApiResponse): BrandingPayload => {
  const applicationTitle =
    payload.applicationTitle ??
    payload.application_title ??
    DEFAULT_BRANDING.applicationTitle;

  const faviconUrl =
    payload.faviconUrl ??
    payload.favicon_url ??
    payload.favicon ??
    DEFAULT_BRANDING.faviconUrl;

  const appleTouchIconUrl =
    payload.appleTouchIconUrl ??
    payload.apple_touch_icon_url ??
    payload.appleTouchIcon ??
    DEFAULT_BRANDING.appleTouchIconUrl;

  const manifestUrl =
    payload.manifestUrl ??
    payload.manifest_url ??
    payload.manifest ??
    DEFAULT_BRANDING.manifestUrl;

  return {
    applicationTitle,
    faviconUrl,
    appleTouchIconUrl,
    manifestUrl,
  };
};

const extractEnvironmentSuffix = (
  payload: BrandingApiResponse
): string | undefined => {
  return (
    (
      payload.environmentSuffix ??
      payload.environment_suffix ??
      undefined
    )?.trim() || undefined
  );
};

export const fetchBranding = async (): Promise<BrandingResult> => {
  try {
    const response = await fetch(BRANDING_ENDPOINT, {
      method: "GET",
      credentials: "include",
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`Branding fetch failed with status ${response.status}`);
    }

    const data = (await response.json()) as BrandingApiResponse;

    return {
      branding: normalisePayload(data),
      environmentSuffix: extractEnvironmentSuffix(data),
      resolvedFromApi: true,
    };
  } catch (error) {
    if (process.env.NODE_ENV === "development") {
      console.warn("[branding] falling back to defaults", error);
    }
    return { branding: DEFAULT_BRANDING, resolvedFromApi: false };
  }
};
