export interface BrandingPayload {
  /**
   * Human readable application title shown in the document title.
   */
  applicationTitle: string;
  /**
   * Primary favicon url (png/ico/svg).
   */
  faviconUrl: string;
  /**
   * Optional apple touch icon url for iOS home screen shortcuts.
   */
  appleTouchIconUrl?: string;
  /**
   * Optional manifest link to swap when branding is customised.
   */
  manifestUrl?: string;
}

export interface BrandingState {
  branding: BrandingPayload;
  isLoading: boolean;
  environmentSuffix?: string;
  environment?: string;
  version?: string;
}

export interface BrandingResult {
  branding: BrandingPayload;
  environmentSuffix?: string;
  environment?: string;
  version?: string;
  resolvedFromEnv: boolean;
}
