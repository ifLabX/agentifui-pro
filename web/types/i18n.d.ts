import type { Locale } from "@/i18n/config";

type CommonMessages = typeof import("../messages/en-US/common.json");
type AuthMessages = typeof import("../messages/en-US/auth.json");
type ChatMessages = typeof import("../messages/en-US/chat.json");

export type Messages = {
  "common": CommonMessages;
  "auth": AuthMessages;
  "chat": ChatMessages;
};

export type { Locale };
