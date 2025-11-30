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

export interface BrandingApiResponse {
  application_title?: string;
  favicon_url?: string;
  apple_touch_icon_url?: string;
  manifest_url?: string;
  environment_suffix?: string;
}

export interface BrandingState {
  branding: BrandingPayload;
  isLoading: boolean;
  environmentSuffix?: string;
}

export interface BrandingResult {
  branding: BrandingPayload;
  environmentSuffix?: string;
  resolvedFromApi: boolean;
}
