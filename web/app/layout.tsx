import type { Metadata } from "next";
import { AppProviders } from "@/providers/app-providers";
import { getLocale, getMessages } from "next-intl/server";

import { geistMono, geistSans, inter, playfairDisplay } from "@/lib/fonts";
import { cn } from "@/lib/utils";

import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "AgentifUI",
    template: "%s - AgentifUI",
  },
  description: "AgentifUI control center",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getLocale();
  const messages = await getMessages();

  return (
    <html
      lang={locale}
      className={cn(
        geistSans.variable,
        geistMono.variable,
        inter.variable,
        playfairDisplay.variable
      )}
      suppressHydrationWarning
    >
      <body className="min-h-screen bg-background font-sans antialiased">
        <AppProviders locale={locale} messages={messages}>
          {children}
        </AppProviders>
      </body>
    </html>
  );
}
