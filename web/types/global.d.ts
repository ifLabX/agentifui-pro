import type { Locale } from "@/i18n/config";

// Define the namespace structure that matches our i18n/request.ts loading pattern
type CommonMessages = typeof import("../messages/en-US/common.json");
type AuthMessages = typeof import("../messages/en-US/auth.json");

// Create the full message structure with namespace keys
type Messages = {
  common: CommonMessages;
  auth: AuthMessages;
};

// Extend next-intl types
declare module "next-intl" {
  interface AppConfig {
    Locale: Locale;
    Messages: Messages;
  }
}
