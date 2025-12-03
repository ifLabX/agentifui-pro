"use client";

import { create } from "zustand";

import type { BrandingPayload } from "@/types/branding";
import { BRANDING_FROM_ENV, DEFAULT_BRANDING } from "@/config/branding";

type BrandingStore = {
  branding: BrandingPayload;
  isLoading: boolean;
  environmentSuffix?: string;
  environment?: string;
  version?: string;
  setBranding: (payload: BrandingPayload) => void;
  setLoading: (value: boolean) => void;
  setEnvironmentSuffix: (value?: string) => void;
  setEnvironment: (value?: string) => void;
  setVersion: (value?: string) => void;
};

export const useBrandingStore = create<BrandingStore>(set => ({
  branding: BRANDING_FROM_ENV.branding ?? DEFAULT_BRANDING,
  isLoading: false,
  environmentSuffix: BRANDING_FROM_ENV.environmentSuffix,
  environment: BRANDING_FROM_ENV.environment,
  version: BRANDING_FROM_ENV.version,
  setBranding: payload => set({ branding: payload }),
  setLoading: value => set({ isLoading: value }),
  setEnvironmentSuffix: value => set({ environmentSuffix: value }),
  setEnvironment: value => set({ environment: value }),
  setVersion: value => set({ version: value }),
}));

export type { BrandingPayload } from "@/types/branding";
