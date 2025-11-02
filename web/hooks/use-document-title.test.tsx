import { useBrandingStore } from "@/stores/branding-store";
import { renderHook, waitFor } from "@testing-library/react";

import { DEFAULT_BRANDING } from "@/config/branding";

import { useDocumentTitle } from "./use-document-title";

const resetDocumentHead = () => {
  document.title = "";
  document
    .querySelectorAll('link[data-branding-managed="true"]')
    .forEach(node => node.remove());
};

describe("useDocumentTitle", () => {
  beforeEach(() => {
    resetDocumentHead();
    useBrandingStore.setState({
      branding: DEFAULT_BRANDING,
      isLoading: true,
      environmentSuffix: undefined,
    });
  });

  it("keeps title empty while branding is loading", async () => {
    renderHook(() => useDocumentTitle({ title: "Dashboard" }));

    await waitFor(() => {
      expect(document.title).toBe("");
    });
  });

  it("applies default branding once loaded", async () => {
    useBrandingStore.setState({ isLoading: false });

    renderHook(() => useDocumentTitle({ title: "Dashboard" }));

    await waitFor(() => {
      expect(document.title).toBe("Dashboard - AgentifUI");
    });
  });

  it("supports disabling branding suffix", async () => {
    useBrandingStore.setState({ isLoading: false });

    renderHook(() =>
      useDocumentTitle({ title: "Dashboard", disableBranding: true })
    );

    await waitFor(() => {
      expect(document.title).toBe("Dashboard");
    });
  });

  it("uses custom branding values", async () => {
    useBrandingStore.setState({
      isLoading: false,
      branding: {
        applicationTitle: "ExampleBrand",
        faviconUrl: "/custom.ico",
        appleTouchIconUrl: "/custom-apple.png",
        manifestUrl: "/custom.webmanifest",
      },
    });

    renderHook(() => useDocumentTitle({ title: "Inbox" }));

    await waitFor(() => {
      expect(document.title).toBe("Inbox - ExampleBrand");
      const icons = document.querySelectorAll(
        'link[data-branding-managed="true"]'
      );
      expect(icons.length).toBeGreaterThan(0);
    });
  });

  it("appends environment suffix", async () => {
    useBrandingStore.setState({
      isLoading: false,
      environmentSuffix: "[Staging]",
    });

    renderHook(() => useDocumentTitle({ title: "Dashboard" }));

    await waitFor(() => {
      expect(document.title).toBe("Dashboard - AgentifUI [Staging]");
    });
  });
});
