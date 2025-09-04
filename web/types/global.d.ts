import type { Locale, Messages } from "./i18n";

// Extend next-intl types with our centralized i18n configuration
declare module "next-intl" {
  interface AppConfig {
    Locale: Locale;
    Messages: Messages;
  }
}
