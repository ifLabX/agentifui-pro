"use client";

import { createWithEqualityFn } from "zustand/traditional";

import type { BrandingPayload } from "@/types/branding";
import { DEFAULT_BRANDING } from "@/config/branding";

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

export const useBrandingStore = createWithEqualityFn<BrandingStore>(set => ({
  branding: DEFAULT_BRANDING,
  isLoading: true,
  environmentSuffix: undefined,
  environment: undefined,
  version: undefined,
  setBranding: payload => set({ branding: payload }),
  setLoading: value => set({ isLoading: value }),
  setEnvironmentSuffix: value => set({ environmentSuffix: value }),
  setEnvironment: value => set({ environment: value }),
  setVersion: value => set({ version: value }),
}));

export type { BrandingPayload } from "@/types/branding";
