import { cookies } from "next/headers";
import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";

import { defaultLocale, locales, namespaces, type Locale } from "./config";

/**
 * Dynamic message loading utility
 * Loads multiple namespace files and merges them into a single flat object
 * File structure: auth.json -> auth: { SignIn: {...}, SignUp: {...} }
 */
async function loadMessages(locale: Locale) {
  const messages: Record<string, unknown> = {};

  for (const namespace of namespaces) {
    try {
      const moduleMessages = (
        await import(`../messages/${locale}/${namespace}.json`)
      ).default;
      // Create namespace structure: auth.SignIn, common.Navigation, etc.
      messages[namespace] = moduleMessages;
    } catch (error) {
      console.error(
        `Failed to load ${namespace} messages for locale ${locale}:`,
        error
      );
    }
  }

  return messages;
}

/**
 * Get locale from storage (cookies, user settings, etc.)
 */
async function getLocaleFromStorage(): Promise<Locale> {
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get("locale")?.value;

  // Return cookie value if valid, otherwise default
  return hasLocale(locales, localeCookie) ? localeCookie : defaultLocale;
}

export default getRequestConfig(async () => {
  // Get locale from storage (cookies, user settings, etc.)
  const locale = await getLocaleFromStorage();

  return {
    locale,
    messages: await loadMessages(locale),
  };
});
