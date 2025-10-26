import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const fontVars = {
  sans: "var(--font-geist-sans)",
  mono: "var(--font-geist-mono)",
  inter: "var(--font-inter)",
  serif: "var(--font-serif)",
};

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        chart: {
          1: "hsl(var(--chart-1))",
          2: "hsl(var(--chart-2))",
          3: "hsl(var(--chart-3))",
          4: "hsl(var(--chart-4))",
          5: "hsl(var(--chart-5))",
        },
        "chat-input-bg": "hsl(var(--chat-input-bg))",
        "chat-input-border": "hsl(var(--chat-input-border))",
        "chat-input-text": "hsl(var(--chat-input-text))",
        "chat-input-placeholder": "hsl(var(--chat-input-placeholder))",
        "chat-button-bg": "hsl(var(--chat-button-bg))",
        "chat-button-border": "hsl(var(--chat-button-border))",
        "chat-button-text": "hsl(var(--chat-button-text))",
        "chat-button-hover-bg": "hsl(var(--chat-button-hover-bg))",
        "chat-submit-bg": "hsl(var(--chat-submit-bg))",
        "chat-submit-text": "hsl(var(--chat-submit-text))",
        "chat-submit-hover-bg": "hsl(var(--chat-submit-hover-bg))",
        "chat-submit-disabled-bg": "hsl(var(--chat-submit-disabled-bg))",
        "chat-submit-disabled-text": "hsl(var(--chat-submit-disabled-text))",
        "chat-attachment-bg": "hsl(var(--chat-attachment-bg))",
        "chat-attachment-border": "hsl(var(--chat-attachment-border))",
        "chat-attachment-text": "hsl(var(--chat-attachment-text))",
        "chat-attachment-text-secondary":
          "hsl(var(--chat-attachment-text-secondary))",
        "chat-attachment-remove-bg": "hsl(var(--chat-attachment-remove-bg))",
        "chat-attachment-remove-hover-bg":
          "hsl(var(--chat-attachment-remove-hover-bg))",
        "chat-error-border": "hsl(var(--chat-error-border))",
        "chat-error-text": "hsl(var(--chat-error-text))",
      },
      fontFamily: {
        sans: [
          fontVars.sans,
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "PingFang SC",
          "Microsoft YaHei",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        mono: [
          fontVars.mono,
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Consolas",
          "Monaco",
          "Courier New",
          "monospace",
        ],
        inter: [fontVars.inter, "system-ui", "sans-serif"],
        serif: [
          fontVars.serif,
          "ui-serif",
          "Georgia",
          "Times New Roman",
          "Times",
          "serif",
        ],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [animate],
};

export default config;
