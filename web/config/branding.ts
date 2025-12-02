import type { BrandingPayload } from "@/types/branding";

export const DEFAULT_BRANDING: BrandingPayload = {
  applicationTitle: "AgentifUI",
  faviconUrl: "/favicon.ico",
};

export const BRANDING_QUERY_KEY = ["branding"] as const;

export const BRANDING_ENDPOINT = "/branding";
