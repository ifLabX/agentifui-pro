import { getTranslations } from "next-intl/server";

export async function ServerTestComponent() {
  const t = await getTranslations();

  return (
    <div className="mt-4 p-3 bg-gray-50 rounded">
      <h4 className="font-medium text-gray-800 mb-2">
        Server Component Examples
      </h4>

      <div className="space-y-2 text-sm">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          <span className="text-green-600">{t("common.messages.success")}</span>
        </div>

        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 bg-red-500 rounded-full"></span>
          <span className="text-red-600">{t("common.messages.error")}</span>
        </div>

        <nav className="flex space-x-4 text-blue-600">
          <a href="#" className="hover:underline">
            {t("common.navigation.home")}
          </a>
          <a href="#" className="hover:underline">
            {t("common.navigation.about")}
          </a>
          <a href="#" className="hover:underline">
            {t("common.navigation.contact")}
          </a>
        </nav>

        <div className="p-2 border rounded">
          <h5 className="font-medium">{t("auth.sign-up.title")}</h5>
          <p className="text-xs text-gray-600">
            {t("auth.sign-up.has-account")}
          </p>
        </div>
      </div>

      <div className="text-xs text-gray-500 mt-2 border-t pt-2">
        <p>This component tests:</p>
        <ul className="list-disc list-inside ml-2">
          <li>Server-side getTranslations usage</li>
          <li>Single t function with kebab-case keys</li>
          <li>Async translation loading</li>
        </ul>
      </div>
    </div>
  );
}
