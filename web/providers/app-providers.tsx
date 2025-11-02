"use client";

import { useState, type PropsWithChildren } from "react";
import type { Locale } from "@/i18n/config";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";

import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/theme-provider";

import { BrandingProvider } from "./branding-provider";

type AppProvidersProps = PropsWithChildren<{
  locale: Locale;
  messages: AbstractIntlMessages;
}>;

export function AppProviders({
  children,
  locale,
  messages,
}: AppProvidersProps) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider delayDuration={100} skipDelayDuration={300}>
          <NextIntlClientProvider locale={locale} messages={messages}>
            <BrandingProvider>{children}</BrandingProvider>
          </NextIntlClientProvider>
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default AppProviders;
