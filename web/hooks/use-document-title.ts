"use client";

import { useEffect, useMemo } from "react";
import { useBrandingStore } from "@/stores/branding-store";
import { useTitle } from "ahooks";
import { shallow } from "zustand/shallow";

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
  const { branding, isLoading, environmentSuffix } = useBrandingStore(
    state => ({
      branding: state.branding,
      isLoading: state.isLoading,
      environmentSuffix: state.environmentSuffix,
    }),
    shallow
  );

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

  const resolvedTitle = useMemo(() => {
    if (isLoading) {
      return loadingTitle ?? formattedTitle;
    }

    return formattedTitle;
  }, [isLoading, loadingTitle, formattedTitle]);

  useTitle(resolvedTitle);

  const favicon = branding.faviconUrl || DEFAULT_BRANDING.faviconUrl;
  const appleTouchIcon =
    branding.appleTouchIconUrl || DEFAULT_BRANDING.appleTouchIconUrl;
  const manifest = branding.manifestUrl || DEFAULT_BRANDING.manifestUrl;

  useEffect(() => {
    setFaviconLinks({
      favicon,
      appleTouchIcon,
      manifest,
    });
  }, [favicon, appleTouchIcon, manifest]);
};

export default useDocumentTitle;
