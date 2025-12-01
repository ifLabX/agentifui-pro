"use client";

import { useState, type PropsWithChildren } from "react";
import type { Locale } from "@/i18n/config";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";

import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/theme-provider";

import { BrandingProvider } from "./branding-provider";

type AppProvidersProps = PropsWithChildren<{
  locale: Locale;
  messages: AbstractIntlMessages;
  timeZone: string;
}>;

export function AppProviders({
  children,
  locale,
  messages,
  timeZone,
}: AppProvidersProps) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider delayDuration={100} skipDelayDuration={300}>
          <NextIntlClientProvider
            locale={locale}
            messages={messages}
            timeZone={timeZone}
          >
            <BrandingProvider>{children}</BrandingProvider>
          </NextIntlClientProvider>
        </TooltipProvider>
      </ThemeProvider>
      {process.env.NODE_ENV === "development" && (
        <ReactQueryDevtools
          initialIsOpen={false}
          buttonPosition="bottom-right"
        />
      )}
    </QueryClientProvider>
  );
}

export default AppProviders;
