import type {
  BrandingApiResponse,
  BrandingPayload,
  BrandingResult,
} from "@/types/branding";
import {
  BRANDING_ENDPOINT,
  BRANDING_QUERY_KEY,
  DEFAULT_BRANDING,
} from "@/config/branding";
import { api } from "@/lib/api-client";

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
  const suffix = payload.environmentSuffix ?? payload.environment_suffix;

  if (suffix === undefined || suffix === null) {
    return undefined;
  }

  return suffix.trim();
};

export const fetchBranding = async (): Promise<BrandingResult> => {
  try {
    const data = await api.get<BrandingApiResponse>(BRANDING_ENDPOINT, {
      cache: "no-store",
    });

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

export const brandingQueryOptions = () => ({
  queryKey: BRANDING_QUERY_KEY,
  queryFn: fetchBranding,
  staleTime: 10 * 60 * 1000,
});
