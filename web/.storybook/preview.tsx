import type { Preview } from "@storybook/react-vite";
import { NextIntlClientProvider } from "next-intl";
import ResizeObserver from "resize-observer-polyfill";

import { Theme } from "@/types/app";
import { ThemeProvider } from "@/components/theme-provider";

import "../app/globals.css";

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
      name: "Theme",
      description: "Global theme for components",
      defaultValue: Theme.system,
      toolbar: {
        icon: "mirror",
        items: [
          { value: Theme.light, icon: "sun", title: "Light" },
          { value: Theme.dark, icon: "moon", title: "Dark" },
          { value: Theme.system, icon: "browser", title: "System" },
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
    backgrounds: {
      default: Theme.light,
      values: [
        { name: Theme.light, value: "#ffffff" },
        { name: Theme.dark, value: "#1a1a1a" },
      ],
    },
  },

  decorators: [
    (Story, context) => {
      const activeTheme =
        (context.globals.theme as Theme | undefined) ?? Theme.system;
      const forcedTheme =
        activeTheme === Theme.system ? undefined : activeTheme;

      const backgroundName =
        activeTheme === Theme.dark ? Theme.dark : Theme.light;

      if (context.parameters.backgrounds) {
        context.parameters.backgrounds.default = backgroundName;
      }

      return (
        <ThemeProvider forcedTheme={forcedTheme}>
          <NextIntlClientProvider locale="en" messages={messages}>
            <Story />
          </NextIntlClientProvider>
        </ThemeProvider>
      );
    },
  ],
};

export default preview;
