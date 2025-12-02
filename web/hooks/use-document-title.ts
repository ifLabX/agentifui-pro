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
    console.log("[useDocumentTitle] Effect triggered:", {
      isLoading,
      loadingTitle,
      formattedTitle,
      currentTitle: document.title,
    });

    if (isLoading) {
      if (loadingTitle) {
        console.log("[useDocumentTitle] Setting loading title:", loadingTitle);
        document.title = loadingTitle;
      } else {
        console.log(
          "[useDocumentTitle] Loading but no loadingTitle, preserving:",
          document.title
        );
      }
      return;
    }

    if (formattedTitle) {
      console.log(
        "[useDocumentTitle] Setting formatted title:",
        formattedTitle
      );
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
