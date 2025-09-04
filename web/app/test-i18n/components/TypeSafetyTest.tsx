"use client";

import { useTranslations } from "next-intl";

export function TypeSafetyTest() {
  const t = useTranslations();

  return (
    <div className="border p-4 rounded">
      <h3 className="font-medium mb-2">TypeScript Type Safety Test</h3>

      <div className="space-y-2 text-sm">
        {/* Valid keys - should work */}
        <p className="text-green-600">
          ✅ Valid: {t("common.navigation.home")}
        </p>
        <p className="text-green-600">✅ Valid: {t("auth.sign-in.email")}</p>

        {/* Invalid keys - should show TypeScript errors in IDE */}
        {/* 
        <p className="text-red-600">❌ Invalid: {t('common.navigation.invalid-key')}</p>
        <p className="text-red-600">❌ Invalid: {t('auth.sign-in.wrong-key')}</p>
        */}

        <div className="mt-4 p-2 bg-gray-100 rounded text-xs">
          <p className="font-medium">Type Safety Features:</p>
          <ul className="list-disc list-inside mt-1">
            <li>Autocomplete for valid message keys</li>
            <li>TypeScript errors for invalid keys</li>
            <li>Proper locale type checking</li>
            <li>Message structure validation</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
