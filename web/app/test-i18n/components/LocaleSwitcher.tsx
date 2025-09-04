"use client";

import { useState, useTransition } from "react";
import { localeNames, locales, type Locale } from "@/i18n/config";
import { setLocale } from "@/i18n/locale-actions";
import { useTranslations } from "next-intl";

export function LocaleSwitcher() {
  const [isPending, startTransition] = useTransition();
  const [currentLocale, setCurrentLocale] = useState<Locale>("en-US");
  const t = useTranslations();

  const handleLocaleChange = (locale: Locale) => {
    setCurrentLocale(locale);
    startTransition(async () => {
      await setLocale(locale);
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {locales.map(locale => (
          <button
            key={locale}
            onClick={() => handleLocaleChange(locale)}
            disabled={isPending}
            className={`px-4 py-2 rounded border transition-colors ${
              currentLocale === locale
                ? "bg-blue-500 text-white border-blue-500"
                : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
            } ${isPending ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          >
            {localeNames[locale]}
          </button>
        ))}
      </div>

      <p className="text-sm text-gray-600">
        {isPending
          ? t("common.actions.loading")
          : `Current: ${localeNames[currentLocale]}`}
      </p>

      <div className="text-xs text-gray-500">
        <p>This component tests:</p>
        <ul className="list-disc list-inside ml-2">
          <li>Client-side locale switching</li>
          <li>useTranslations hook</li>
          <li>Server action integration</li>
          <li>Loading states with useTransition</li>
        </ul>
      </div>
    </div>
  );
}
