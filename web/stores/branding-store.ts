"use client";

import { createWithEqualityFn } from "zustand/traditional";

import type { BrandingPayload } from "@/types/branding";
import { BRANDING_ENV_SUFFIX, DEFAULT_BRANDING } from "@/config/branding";

type BrandingStore = {
  branding: BrandingPayload;
  isLoading: boolean;
  environmentSuffix?: string;
  setBranding: (payload: BrandingPayload) => void;
  setLoading: (value: boolean) => void;
  setEnvironmentSuffix: (value?: string) => void;
};

export const useBrandingStore = createWithEqualityFn<BrandingStore>(set => ({
  branding: DEFAULT_BRANDING,
  isLoading: true,
  environmentSuffix: BRANDING_ENV_SUFFIX,
  setBranding: payload => set({ branding: payload }),
  setLoading: value => set({ isLoading: value }),
  setEnvironmentSuffix: value => set({ environmentSuffix: value }),
}));

export type { BrandingPayload } from "@/types/branding";
