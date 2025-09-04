/**
 * Centralized locale and namespace configuration
 * All locale and namespace additions should be made here
 */

// Supported locales following next-intl best practices
export const locales = ["en-US", "zh-Hans", "ja-JP"] as const;
export type Locale = (typeof locales)[number];

// Default locale
export const defaultLocale: Locale = "en-US";

// Namespaces - add new namespaces here only
export const namespaces = ["common", "auth"] as const;
export type Namespace = (typeof namespaces)[number];

// Locale display names
export const localeNames: Record<Locale, string> = {
  "en-US": "English",
  "zh-Hans": "Chinese (Simplified)",
  "ja-JP": "Japanese",
} as const;

// Locale metadata
export const localeInfo: Record<
  Locale,
  {
    dir: "ltr" | "rtl";
  }
> = {
  "en-US": { dir: "ltr" },
  "zh-Hans": { dir: "ltr" },
  "ja-JP": { dir: "ltr" },
} as const;
