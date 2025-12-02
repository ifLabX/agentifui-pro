"use client";

import { useEffect, useMemo } from "react";
import { useBrandingStore } from "@/stores/branding-store";

import { DEFAULT_BRANDING } from "@/config/branding";
import { setFaviconLinks } from "@/lib/favicon";
import { formatTitle } from "@/lib/title";

const DEFAULT_SEPARATOR = " - ";

export type UseDocumentTitleOptions = {
  title?: string;
  suffix?: string;
  separator?: string;
  disableBranding?: boolean;
  loadingTitle?: string;
};

export const useDocumentTitle = ({
  title,
  suffix,
  separator = DEFAULT_SEPARATOR,
  disableBranding = false,
  loadingTitle,
}: UseDocumentTitleOptions = {}) => {
  const branding = useBrandingStore(state => state.branding);
  const isLoading = useBrandingStore(state => state.isLoading);
  const environmentSuffix = useBrandingStore(state => state.environmentSuffix);

  const computedSuffix = suffix ?? environmentSuffix;

  const brand = disableBranding ? undefined : branding.applicationTitle;

  const formattedTitle = useMemo(
    () =>
      formatTitle({
        title,
        brand,
        suffix: computedSuffix,
        separator,
      }),
    [title, brand, computedSuffix, separator]
  );

  useEffect(() => {
    if (isLoading) {
      if (loadingTitle) {
        document.title = loadingTitle;
      }
      return;
    }

    if (formattedTitle) {
      document.title = formattedTitle;
    }
  }, [isLoading, loadingTitle, formattedTitle]);

  const favicon = branding.faviconUrl || DEFAULT_BRANDING.faviconUrl;
  const appleTouchIcon = branding.appleTouchIconUrl;
  const manifest = branding.manifestUrl;

  useEffect(() => {
    setFaviconLinks({
      favicon,
      appleTouchIcon,
      manifest,
    });
  }, [favicon, appleTouchIcon, manifest]);
};

export default useDocumentTitle;
