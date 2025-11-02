import type { BrandingPayload } from "@/types/branding";

export const DEFAULT_BRANDING: BrandingPayload = {
  applicationTitle: "AgentifUI",
  faviconUrl: "/favicon.ico",
  appleTouchIconUrl: "/apple-touch-icon.png",
  manifestUrl: "/manifest.json",
};

export const BRANDING_ENV_SUFFIX =
  process.env.NEXT_PUBLIC_APP_ENV_SUFFIX?.trim() || undefined;

export const BRANDING_QUERY_KEY = ["branding"] as const;

export const BRANDING_ENDPOINT =
  process.env.NEXT_PUBLIC_BRANDING_ENDPOINT?.trim() || "/api/branding";
