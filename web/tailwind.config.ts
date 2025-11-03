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
        background: "var(--background)",
        foreground: "var(--foreground)",
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        destructive: {
          DEFAULT: "var(--destructive)",
          foreground: "var(--destructive-foreground)",
        },
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        accent: {
          DEFAULT: "var(--accent)",
          foreground: "var(--accent-foreground)",
        },
        popover: {
          DEFAULT: "var(--popover)",
          foreground: "var(--popover-foreground)",
        },
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
          border: "var(--card-border)",
        },
        chart: {
          1: "var(--chart-1)",
          2: "var(--chart-2)",
          3: "var(--chart-3)",
          4: "var(--chart-4)",
          5: "var(--chart-5)",
        },
        "chat-input-bg": "var(--chat-input-bg)",
        "chat-input-border": "var(--chat-input-border)",
        "chat-input-text": "var(--chat-input-text)",
        "chat-input-placeholder": "var(--chat-input-placeholder)",
        "chat-button-bg": "var(--chat-button-bg)",
        "chat-button-border": "var(--chat-button-border)",
        "chat-button-text": "var(--chat-button-text)",
        "chat-button-hover-bg": "var(--chat-button-hover-bg)",
        "chat-submit-bg": "var(--chat-submit-bg)",
        "chat-submit-text": "var(--chat-submit-text)",
        "chat-submit-hover-bg": "var(--chat-submit-hover-bg)",
        "chat-submit-disabled-bg": "var(--chat-submit-disabled-bg)",
        "chat-submit-disabled-text": "var(--chat-submit-disabled-text)",
        "chat-attachment-bg": "var(--chat-attachment-bg)",
        "chat-attachment-border": "var(--chat-attachment-border)",
        "chat-attachment-text": "var(--chat-attachment-text)",
        "chat-attachment-text-secondary":
          "var(--chat-attachment-text-secondary)",
        "chat-attachment-remove-bg": "var(--chat-attachment-remove-bg)",
        "chat-attachment-remove-hover-bg":
          "var(--chat-attachment-remove-hover-bg)",
        "chat-error-border": "var(--chat-error-border)",
        "chat-error-text": "var(--chat-error-text)",
        "kbd-bg": "var(--kbd-bg)",
        "kbd-border": "var(--kbd-border)",
        "kbd-text": "var(--kbd-text)",
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
