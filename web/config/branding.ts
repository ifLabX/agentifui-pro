import type { BrandingPayload, BrandingResult } from "@/types/branding";

export const DEFAULT_BRANDING: BrandingPayload = {
  applicationTitle: "AgentifUI",
  faviconUrl: "/favicon.ico",
};

const sanitize = (value?: string | null): string | undefined => {
  if (!value) return undefined;
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
};

const readPublicEnv = (key: string): string | undefined =>
  sanitize(process.env[key as keyof NodeJS.ProcessEnv] as string | undefined);

export const resolveBrandingFromEnv = (): BrandingResult => {
  const applicationTitle =
    readPublicEnv("NEXT_PUBLIC_BRANDING_APPLICATION_TITLE") ||
    DEFAULT_BRANDING.applicationTitle;
  const faviconUrl =
    readPublicEnv("NEXT_PUBLIC_BRANDING_FAVICON_URL") ||
    DEFAULT_BRANDING.faviconUrl;
  const appleTouchIconUrl = readPublicEnv(
    "NEXT_PUBLIC_BRANDING_APPLE_TOUCH_ICON_URL"
  );
  const manifestUrl = readPublicEnv("NEXT_PUBLIC_BRANDING_MANIFEST_URL");

  return {
    branding: {
      applicationTitle,
      faviconUrl,
      appleTouchIconUrl,
      manifestUrl,
    },
    environmentSuffix: readPublicEnv("NEXT_PUBLIC_BRANDING_ENVIRONMENT_SUFFIX"),
    environment:
      readPublicEnv("NEXT_PUBLIC_APP_ENVIRONMENT") ||
      process.env.NODE_ENV ||
      "development",
    version:
      readPublicEnv("NEXT_PUBLIC_APP_VERSION") ||
      readPublicEnv("NEXT_PUBLIC_VERSION") ||
      "unknown",
    resolvedFromEnv: true,
  };
};

export const BRANDING_FROM_ENV = resolveBrandingFromEnv();
