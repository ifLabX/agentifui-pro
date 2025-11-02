"use client";

import { useTranslations } from "next-intl";

import { useDocumentTitle } from "@/hooks/use-document-title";
import { ChatInput } from "@/components/ui/chat-input";

export default function Home() {
  const t = useTranslations("common.navigation");
  useDocumentTitle({ title: t("home") });

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-background">
      <div className="w-full max-w-4xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-foreground">
            Chat Input Component
          </h1>
          <p className="text-muted-foreground">
            A minimalist chat input with attachment support using design tokens
          </p>
        </div>

        <ChatInput placeholder="Type your message..." />

        <div className="text-center text-sm text-muted-foreground">
          <p>Press Enter to send • Shift + Enter for new line</p>
        </div>
      </div>
    </main>
  );
}
