import { useEffect } from "react";
import type { Preview } from "@storybook/react-vite";
import { NextIntlClientProvider } from "next-intl";
import ResizeObserver from "resize-observer-polyfill";

import { ThemeProvider } from "@/components/theme-provider";

import "../app/globals.css";

// Global styles component to sync Storybook background with theme
function GlobalStyles({ theme }: { theme?: string }) {
  useEffect(() => {
    const isDark = theme === "dark";
    const bgColor = isDark ? "oklch(0.13 0.006 95)" : "oklch(0.99 0.002 95)";
    const textColor = isDark ? "oklch(0.96 0.008 95)" : "oklch(0.2 0.006 95)";

    // Update Storybook canvas background
    document.body.style.backgroundColor = bgColor;
    document.body.style.color = textColor;

    // Also update the docs page if it exists
    document.querySelectorAll<HTMLElement>(".docs-story").forEach(storyEl => {
      storyEl.style.backgroundColor = bgColor;
      storyEl.style.color = textColor;
    });
  }, [theme]);

  return null;
}

// Mock next-intl messages for Storybook
const messages = {
  common: {
    navigation: {
      home: "Home",
    },
  },
  auth: {
    "sign-in": {
      email: "Email",
      password: "Password",
    },
  },
  chat: {
    input: {
      placeholder: "Type a message...",
    },
    dropzone: {
      label: "Drop files here",
    },
    attachments: {
      "file-size-zero": "0 bytes",
      units: {
        bytes: "B",
        kilobytes: "KB",
        megabytes: "MB",
        gigabytes: "GB",
      },
      "remove-aria": "Remove attachment",
      "upload-aria": "Upload files",
      "add-aria": "Add attachments",
    },
    submit: {
      "aria-label": "Send message",
    },
  },
};

// Polyfills for Radix UI and Floating UI
if (typeof window !== "undefined") {
  // PointerEvent polyfill for older browsers
  if (!window.PointerEvent) {
    class PointerEvent extends MouseEvent {
      public pointerId: number;
      public width: number;
      public height: number;
      public pressure: number;
      public tangentialPressure: number;
      public tiltX: number;
      public tiltY: number;
      public twist: number;
      public pointerType: string;
      public isPrimary: boolean;

      constructor(type: string, params: PointerEventInit = {}) {
        super(type, params);
        this.pointerId = params.pointerId || 0;
        this.width = params.width || 0;
        this.height = params.height || 0;
        this.pressure = params.pressure || 0;
        this.tangentialPressure = params.tangentialPressure || 0;
        this.tiltX = params.tiltX || 0;
        this.tiltY = params.tiltY || 0;
        this.twist = params.twist || 0;
        this.pointerType = params.pointerType || "";
        this.isPrimary = params.isPrimary || false;
      }
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (window as any).PointerEvent = PointerEvent;
  }

  // ResizeObserver polyfill
  if (!window.ResizeObserver) {
    window.ResizeObserver = ResizeObserver as typeof window.ResizeObserver;
  }

  // URL.createObjectURL polyfill for file handling
  if (!window.URL.createObjectURL) {
    window.URL.createObjectURL = (_blob: Blob | MediaSource) => {
      return `blob:${Math.random().toString(36).substring(7)}`;
    };
  }

  if (!window.URL.revokeObjectURL) {
    window.URL.revokeObjectURL = () => {};
  }
}

const preview: Preview = {
  globalTypes: {
    theme: {
      description: "Global theme for components",
      toolbar: {
        title: "Theme",
        icon: "circle",
        items: [
          { value: "light", icon: "sun", title: "Light" },
          { value: "dark", icon: "moon", title: "Dark" },
        ],
        dynamicTitle: true,
      },
    },
  },

  parameters: {
    nextjs: {
      appDirectory: true,
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },

  decorators: [
    (Story, context) => {
      const theme = (context.globals.theme as string) || "light";

      return (
        <>
          <GlobalStyles theme={theme} />
          <ThemeProvider
            attribute="class"
            forcedTheme={theme}
            enableSystem={false}
            storageKey="sb-theme"
          >
            <NextIntlClientProvider locale="en" messages={messages}>
              <Story />
            </NextIntlClientProvider>
          </ThemeProvider>
        </>
      );
    },
  ],
};

export default preview;
