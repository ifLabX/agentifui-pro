"use server";

import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { hasLocale } from "next-intl";

import { defaultLocale, locales } from "./config";

/**
 * Server action to set locale in cookies
 */
export async function setLocale(locale: string) {
  // Validate locale
  if (!hasLocale(locales, locale)) {
    throw new Error(`Invalid locale: ${locale}`);
  }

  const cookieStore = await cookies();

  // Set locale cookie (expires in 1 year)
  cookieStore.set("locale", locale, {
    expires: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
    httpOnly: false,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
  });

  // Revalidate to trigger re-rendering with new locale
  revalidatePath("/");
}

/**
 * Server action to get current locale
 */
export async function getLocale(): Promise<string> {
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get("locale")?.value;

  return hasLocale(locales, localeCookie) ? localeCookie : defaultLocale;
}
