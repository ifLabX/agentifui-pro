import type {
  BrandingApiResponse,
  BrandingPayload,
  BrandingResult,
} from "@/types/branding";
import { API_BASE_URL } from "@/config/api";
import { BRANDING_ENDPOINT, DEFAULT_BRANDING } from "@/config/branding";

const toPayload = (payload: BrandingApiResponse): BrandingPayload => ({
  applicationTitle:
    payload.application_title ?? DEFAULT_BRANDING.applicationTitle,
  faviconUrl: payload.favicon_url ?? DEFAULT_BRANDING.faviconUrl,
  appleTouchIconUrl:
    payload.apple_touch_icon_url ?? DEFAULT_BRANDING.appleTouchIconUrl,
  manifestUrl: payload.manifest_url ?? DEFAULT_BRANDING.manifestUrl,
});

const trimOptional = (value?: string): string | undefined =>
  value?.trim() || undefined;

const toBrandingResult = (payload: BrandingApiResponse): BrandingResult => ({
  branding: toPayload(payload),
  environmentSuffix: trimOptional(payload.environment_suffix),
  environment: payload.environment.trim(),
  version: payload.version.trim(),
  resolvedFromApi: true,
});

const buildBrandingUrl = (): string => {
  const baseUrl = API_BASE_URL.replace(/\/+$/, "");
  return `${baseUrl}${BRANDING_ENDPOINT}`;
};

/**
 * Server-side branding fetch with automatic deduplication.
 * Next.js will automatically dedupe identical fetch calls within the same request.
 * Falls back to defaults on error.
 */
export const fetchBrandingServer = async (): Promise<BrandingResult> => {
  try {
    const url = buildBrandingUrl();
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(
        `Branding API failed with status ${response.status}: ${response.statusText}`
      );
    }

    const data: BrandingApiResponse = await response.json();
    return toBrandingResult(data);
  } catch (error) {
    console.error("[branding-server] Failed to fetch branding:", error);

    return {
      branding: DEFAULT_BRANDING,
      environment: process.env.NODE_ENV || "development",
      version: "unknown",
      resolvedFromApi: false,
    };
  }
};
