import { cookies } from "next/headers";
import deepmerge from "deepmerge";
import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";

import { defaultLocale, locales, namespaces, type Locale } from "./config";

async function loadMessages(locale: Locale) {
  const defaultMessages: Record<string, unknown> = {};

  if (locale !== defaultLocale) {
    for (const namespace of namespaces) {
      try {
        const moduleMessages = (
          await import(`../messages/${defaultLocale}/${namespace}.json`)
        ).default;
        defaultMessages[namespace] = moduleMessages;
      } catch {
        defaultMessages[namespace] = {};
      }
    }
  }

  const userMessages: Record<string, unknown> = {};
  for (const namespace of namespaces) {
    try {
      const moduleMessages = (
        await import(`../messages/${locale}/${namespace}.json`)
      ).default;
      userMessages[namespace] = moduleMessages;
    } catch {
      userMessages[namespace] = {};
    }
  }

  return locale !== defaultLocale
    ? deepmerge(defaultMessages, userMessages)
    : userMessages;
}

async function getLocaleFromStorage(): Promise<Locale> {
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get("locale")?.value;
  return hasLocale(locales, localeCookie) ? localeCookie : defaultLocale;
}

export default getRequestConfig(async () => {
  const locale = await getLocaleFromStorage();

  return {
    locale,
    messages: await loadMessages(locale),
    onError() {},
    getMessageFallback({ namespace, key }) {
      const path = [namespace, key].filter(part => part != null).join(".");
      return path;
    },
  };
});
