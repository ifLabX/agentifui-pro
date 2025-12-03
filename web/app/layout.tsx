import type { Metadata } from "next";
import { AppProviders } from "@/providers/app-providers";
import { getLocale, getMessages, getTimeZone } from "next-intl/server";

import { BRANDING_FROM_ENV } from "@/config/branding";
import { geistMono, geistSans, inter, playfairDisplay } from "@/lib/fonts";
import { cn } from "@/lib/utils";

import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: BRANDING_FROM_ENV.branding.applicationTitle,
    template: `%s - ${BRANDING_FROM_ENV.branding.applicationTitle}`,
  },
  description: "AgentifUI control center",
  icons: {
    icon: BRANDING_FROM_ENV.branding.faviconUrl,
    apple: BRANDING_FROM_ENV.branding.appleTouchIconUrl,
  },
  manifest: BRANDING_FROM_ENV.branding.manifestUrl,
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getLocale();
  const messages = await getMessages();
  const timeZone = await getTimeZone();

  return (
    <html
      lang={locale}
      className={cn(
        "h-full",
        geistSans.variable,
        geistMono.variable,
        inter.variable,
        playfairDisplay.variable
      )}
      suppressHydrationWarning
    >
      <body className="h-full bg-background font-sans antialiased">
        <AppProviders
          locale={locale}
          messages={messages}
          timeZone={timeZone}
          initialBranding={BRANDING_FROM_ENV}
        >
          {children}
        </AppProviders>
      </body>
    </html>
  );
}
