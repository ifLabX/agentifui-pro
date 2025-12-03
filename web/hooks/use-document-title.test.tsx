import { useBrandingStore } from "@/stores/branding-store";
import { act, renderHook, waitFor } from "@testing-library/react";

import { DEFAULT_BRANDING } from "@/config/branding";
import { useDocumentTitle } from "@/hooks/use-document-title";

const resetBrandingStore = () => {
  const { setBranding, setEnvironmentSuffix, setLoading } =
    useBrandingStore.getState();
  setBranding({ ...DEFAULT_BRANDING });
  setEnvironmentSuffix(undefined);
  setLoading(true);
};

describe("useDocumentTitle", () => {
  beforeEach(() => {
    document.title = "Test Harness";
    resetBrandingStore();
  });

  it("preserves existing document.title while branding is loading", async () => {
    const { unmount } = renderHook(() =>
      useDocumentTitle({ title: "Dashboard" })
    );

    await waitFor(() => {
      expect(document.title).toBe("Test Harness");
    });

    unmount();
  });

  it("uses provided loadingTitle when loading", async () => {
    const { unmount } = renderHook(() =>
      useDocumentTitle({
        title: "Dashboard",
        loadingTitle: "Loading workspace",
      })
    );

    await waitFor(() => {
      expect(document.title).toBe("Loading workspace");
    });

    unmount();
  });

  it("applies formatted title after loading completes", async () => {
    const { unmount } = renderHook(() =>
      useDocumentTitle({ title: "Dashboard", suffix: "Canary" })
    );

    await waitFor(() => {
      expect(document.title).toBe("Test Harness");
    });

    act(() => {
      useBrandingStore.getState().setLoading(false);
    });

    await waitFor(() => {
      expect(document.title).toBe("Dashboard - AgentifUI Canary");
    });

    unmount();
  });

  it("pulls suffix from store when not provided", async () => {
    const { unmount } = renderHook(() =>
      useDocumentTitle({ title: "Console" })
    );

    act(() => {
      const state = useBrandingStore.getState();
      state.setEnvironmentSuffix("QA");
      state.setLoading(false);
    });

    await waitFor(() => {
      expect(document.title).toBe("Console - AgentifUI QA");
    });

    unmount();
  });

  it("respects disableBranding flag", async () => {
    const { unmount } = renderHook(() =>
      useDocumentTitle({
        title: "Console",
        suffix: "QA",
        disableBranding: true,
      })
    );

    act(() => {
      useBrandingStore.getState().setLoading(false);
    });

    await waitFor(() => {
      expect(document.title).toBe("Console QA");
    });

    unmount();
  });
});
