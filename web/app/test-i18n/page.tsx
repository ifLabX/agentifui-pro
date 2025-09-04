import { getTranslations } from "next-intl/server";

import { ClientTestComponent } from "./components/ClientTestComponent";
import { LocaleSwitcher } from "./components/LocaleSwitcher";
import { ServerTestComponent } from "./components/ServerTestComponent";
import { TypeSafetyTest } from "./components/TypeSafetyTest";

export default async function TestI18nPage() {
  const t = await getTranslations();

  return (
    <div className="container mx-auto p-8 space-y-8">
      <h1 className="text-3xl font-bold">i18n Test Page</h1>

      {/* Locale Switcher */}
      <div className="border p-4 rounded">
        <h2 className="text-xl font-semibold mb-4">Locale Switcher</h2>
        <LocaleSwitcher />
      </div>

      {/* Server Component Tests */}
      <div className="border p-4 rounded">
        <h2 className="text-xl font-semibold mb-4">
          Server Component Translations
        </h2>
        <div className="space-y-2">
          <p>
            <strong>Common Navigation:</strong> {t("common.navigation.home")} |{" "}
            {t("common.navigation.about")} | {t("common.navigation.settings")}
          </p>
          <p>
            <strong>Auth Sign-in:</strong> {t("auth.sign-in.title")} -{" "}
            {t("auth.sign-in.email")}, {t("auth.sign-in.password")}
          </p>
        </div>
        <ServerTestComponent />
      </div>

      {/* Client Component Tests */}
      <div className="border p-4 rounded">
        <h2 className="text-xl font-semibold mb-4">
          Client Component Translations
        </h2>
        <ClientTestComponent />
      </div>

      {/* Type Safety Tests */}
      <TypeSafetyTest />

      {/* Nested Message Tests */}
      <div className="border p-4 rounded">
        <h2 className="text-xl font-semibold mb-4">Namespace Structure Test</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-medium">Common Namespace:</h3>
            <ul className="text-sm space-y-1">
              <li>common.navigation.home: {t("common.navigation.home")}</li>
              <li>common.actions.save: {t("common.actions.save")}</li>
              <li>common.messages.success: {t("common.messages.success")}</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium">Auth Namespace:</h3>
            <ul className="text-sm space-y-1">
              <li>auth.sign-in.title: {t("auth.sign-in.title")}</li>
              <li>auth.sign-up.title: {t("auth.sign-up.title")}</li>
              <li>
                auth.errors.invalid-credentials:{" "}
                {t("auth.errors.invalid-credentials")}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
