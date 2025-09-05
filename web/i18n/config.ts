// Supported locales
export const locales = ["en-US", "zh-Hans", "ja-JP"] as const;
export type Locale = (typeof locales)[number];

// Default locale
export const defaultLocale: Locale = "en-US";

// Namespaces
export const namespaces = ["common", "auth"] as const;
export type Namespace = (typeof namespaces)[number];

// Locale display names
export const localeNames: Record<Locale, string> = {
  "en-US": "English",
  "zh-Hans": "Chinese (Simplified)",
  "ja-JP": "Japanese",
} as const;
