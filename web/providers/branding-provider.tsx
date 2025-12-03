"use client";

import { useLayoutEffect, type PropsWithChildren } from "react";
import { useBrandingStore } from "@/stores/branding-store";

import type { BrandingResult } from "@/types/branding";

type BrandingProviderProps = PropsWithChildren<{
  initialBranding: BrandingResult;
}>;

export function BrandingProvider({
  children,
  initialBranding,
}: BrandingProviderProps) {
  const setBranding = useBrandingStore(state => state.setBranding);
  const setLoading = useBrandingStore(state => state.setLoading);
  const setEnvironmentSuffix = useBrandingStore(
    state => state.setEnvironmentSuffix
  );
  const setEnvironment = useBrandingStore(state => state.setEnvironment);
  const setVersion = useBrandingStore(state => state.setVersion);

  useLayoutEffect(() => {
    setBranding(initialBranding.branding);
    setEnvironmentSuffix(initialBranding.environmentSuffix);
    setEnvironment(initialBranding.environment);
    setVersion(initialBranding.version);
    setLoading(false);
  }, [
    initialBranding,
    setBranding,
    setEnvironmentSuffix,
    setEnvironment,
    setVersion,
    setLoading,
  ]);

  return children;
}
