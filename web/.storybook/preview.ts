import React from "react";
import type { Preview } from "@storybook/react-vite";
import { NextIntlClientProvider } from "next-intl";
import ResizeObserver from "resize-observer-polyfill";

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
      options: {
        light: { name: "light", value: "#ffffff" },
        dark: { name: "dark", value: "#1a1a1a" },
      },
    },
  },

  decorators: [
    Story =>
      React.createElement(
        NextIntlClientProvider,
        { locale: "en", messages },
        React.createElement(Story)
      ),
  ],

  initialGlobals: {
    backgrounds: {
      value: "light",
    },
  },
};

export default preview;
