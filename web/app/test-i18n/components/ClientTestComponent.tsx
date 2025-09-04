"use client";

import { useTranslations } from "next-intl";

export function ClientTestComponent() {
  const t = useTranslations();

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-3 bg-blue-50 rounded">
          <h4 className="font-medium text-blue-800">Common Actions</h4>
          <div className="space-y-1 text-sm">
            <button className="block w-full text-left p-1 hover:bg-blue-100 rounded">
              {t("common.actions.save")}
            </button>
            <button className="block w-full text-left p-1 hover:bg-blue-100 rounded">
              {t("common.actions.cancel")}
            </button>
            <button className="block w-full text-left p-1 hover:bg-blue-100 rounded">
              {t("common.actions.delete")}
            </button>
          </div>
        </div>

        <div className="p-3 bg-green-50 rounded">
          <h4 className="font-medium text-green-800">Auth Form</h4>
          <div className="space-y-2 text-sm">
            <input
              placeholder={t("auth.sign-in.email")}
              className="w-full p-2 border rounded"
              readOnly
            />
            <input
              placeholder={t("auth.sign-in.password")}
              type="password"
              className="w-full p-2 border rounded"
              readOnly
            />
            <button className="w-full p-2 bg-green-600 text-white rounded">
              {t("auth.sign-in.submit")}
            </button>
          </div>
        </div>

        <div className="p-3 bg-red-50 rounded">
          <h4 className="font-medium text-red-800">Error Messages</h4>
          <div className="space-y-1 text-sm text-red-600">
            <p>🚨 {t("auth.errors.email-required")}</p>
            <p>🚨 {t("auth.errors.password-required")}</p>
            <p>🚨 {t("auth.errors.invalid-credentials")}</p>
          </div>
        </div>
      </div>

      <div className="text-xs text-gray-500 border-t pt-2">
        <p>This component tests:</p>
        <ul className="list-disc list-inside ml-2">
          <li>Multiple namespace usage in single component</li>
          <li>useTranslations hook with kebab-case keys</li>
          <li>Interactive UI elements with translations</li>
          <li>Form inputs with translated placeholders</li>
        </ul>
      </div>
    </div>
  );
}
