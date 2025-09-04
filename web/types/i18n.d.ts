import type { Locale } from "@/i18n/config";

type CommonMessages = typeof import("../messages/en-US/common.json");
type AuthMessages = typeof import("../messages/en-US/auth.json");

export type Messages = {
  common: CommonMessages;
  auth: AuthMessages;
};

export type { Locale };
