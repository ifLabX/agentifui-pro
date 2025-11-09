"use client";

import { useEffect, type PropsWithChildren } from "react";
import { brandingQueryOptions } from "@/services/branding";
import { useBrandingStore } from "@/stores/branding-store";
import { useQuery } from "@tanstack/react-query";

import { BRANDING_ENV_SUFFIX } from "@/config/branding";

export function BrandingProvider({ children }: PropsWithChildren) {
  const setBranding = useBrandingStore(state => state.setBranding);
  const setLoading = useBrandingStore(state => state.setLoading);
  const setEnvironmentSuffix = useBrandingStore(
    state => state.setEnvironmentSuffix
  );
  const { data, isPending, error } = useQuery(brandingQueryOptions());

  useEffect(() => {
    setLoading(isPending);
  }, [isPending, setLoading]);

  useEffect(() => {
    if (!data) return;
    setBranding(data.branding);
    if (!data.resolvedFromApi) {
      return;
    }
    if (data.environmentSuffix !== undefined) {
      setEnvironmentSuffix(data.environmentSuffix);
    } else {
      setEnvironmentSuffix(BRANDING_ENV_SUFFIX);
    }
  }, [data, setBranding, setEnvironmentSuffix]);

  useEffect(() => {
    if (!error) return;
    // In error mode we consider branding loading complete to unblock UI.
    setLoading(false);
  }, [error, setLoading]);

  return children;
}
