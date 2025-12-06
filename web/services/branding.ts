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

const trimOptional = (value?: string): string | undefined =>
  value?.trim() || undefined;

const toBrandingResult = (payload: BrandingApiResponse): BrandingResult => ({
  branding: toPayload(payload),
  environmentSuffix: trimOptional(payload.environment_suffix),
  environment: payload.environment.trim(),
  version: payload.version.trim(),
  resolvedFromApi: true,
});

export const fetchBranding = async (): Promise<BrandingResult> =>
  toBrandingResult(await fetchBrandingFromApi());

export const brandingQueryOptions = (initialData?: BrandingResult) => ({
  queryKey: BRANDING_QUERY_KEY,
  queryFn: fetchBranding,
  staleTime: Infinity,
  gcTime: Infinity,
  refetchOnWindowFocus: false,
  refetchOnReconnect: false,
  refetchOnMount: false,
  ...(initialData && {
    initialData,
    enabled: false,
  }),
});

/**
 * Manually refresh branding from API and update store.
 * Alternative: use router.refresh() for full SSR refresh.
 */
export const refreshBranding = async (): Promise<void> => {
  const { useBrandingStore } = await import("@/stores/branding-store");

  try {
    const result = await fetchBranding();

    const store = useBrandingStore.getState();
    store.setBranding(result.branding);

    if (result.resolvedFromApi) {
      store.setEnvironmentSuffix(result.environmentSuffix);
      store.setEnvironment(result.environment);
      store.setVersion(result.version);
    }
  } catch (error) {
    console.error("[branding] Failed to refresh branding:", error);
    throw error;
  }
};
