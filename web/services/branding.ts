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

const fetchBrandingFromApi = () =>
  api.get<BrandingApiResponse>(BRANDING_ENDPOINT, {
    cache: "no-store",
  });

const toPayload = (payload: BrandingApiResponse): BrandingPayload => ({
  applicationTitle:
    payload.application_title ?? DEFAULT_BRANDING.applicationTitle,
  faviconUrl: payload.favicon_url ?? DEFAULT_BRANDING.faviconUrl,
  appleTouchIconUrl:
    payload.apple_touch_icon_url ?? DEFAULT_BRANDING.appleTouchIconUrl,
  manifestUrl: payload.manifest_url ?? DEFAULT_BRANDING.manifestUrl,
});

const normalizeOptional = (value?: string): string | undefined =>
  value?.trim() || undefined;

const extractEnvironmentSuffix = (
  payload: BrandingApiResponse
): string | undefined => normalizeOptional(payload.environment_suffix);

const extractEnvironment = (payload: BrandingApiResponse): string | undefined =>
  normalizeOptional(payload.environment);

const extractVersion = (payload: BrandingApiResponse): string | undefined =>
  normalizeOptional(payload.version);

const toBrandingResult = (payload: BrandingApiResponse): BrandingResult => ({
  branding: toPayload(payload),
  environmentSuffix: extractEnvironmentSuffix(payload),
  environment: extractEnvironment(payload),
  version: extractVersion(payload),
  resolvedFromApi: true,
});

export const fetchBranding = async (): Promise<BrandingResult> =>
  toBrandingResult(await fetchBrandingFromApi());

export const brandingQueryOptions = () => ({
  queryKey: BRANDING_QUERY_KEY,
  queryFn: fetchBranding,
  staleTime: 10 * 60 * 1000,
});
