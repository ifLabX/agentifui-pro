import type { Metadata } from "next";
import { AppProviders } from "@/providers/app-providers";
import { fetchBrandingServer } from "@/services/branding-server";
import { getLocale, getMessages, getTimeZone } from "next-intl/server";

import { geistMono, geistSans, inter, playfairDisplay } from "@/lib/fonts";
import { cn } from "@/lib/utils";

import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const brandingResult = await fetchBrandingServer();
  const { branding } = brandingResult;

  return {
    title: {
      default: branding.applicationTitle,
      template: `%s - ${branding.applicationTitle}`,
    },
    description: "AgentifUI control center",
    icons: {
      icon: branding.faviconUrl,
      apple: branding.appleTouchIconUrl,
    },
    manifest: branding.manifestUrl,
  };
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getLocale();
  const messages = await getMessages();
  const timeZone = await getTimeZone();
  const brandingResult = await fetchBrandingServer();

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
          initialBranding={brandingResult}
        >
          {children}
        </AppProviders>
      </body>
    </html>
  );
}
