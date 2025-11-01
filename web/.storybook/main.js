// eslint-disable-next-line @typescript-eslint/no-require-imports
const path = require("path");

/** @type { import('@storybook/react-vite').StorybookConfig } */
const config = {
  stories: [
    "../components/**/*.stories.@(js|jsx|ts|tsx|mdx)",
    "../app/**/*.stories.@(js|jsx|ts|tsx|mdx)",
  ],

  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
    "@storybook/addon-docs",
  ],

  framework: {
    name: "@storybook/react-vite",
    options: {},
  },

  staticDirs: ["../public"],

  typescript: {
    check: false,
    reactDocgen: "react-docgen-typescript",
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: prop => {
        if (prop.parent) {
          return !prop.parent.fileName.includes("node_modules");
        }
        return true;
      },
    },
  },

  viteFinal: async config => {
    // Configure Vite aliases to match Next.js
    config.resolve = config.resolve || {};
    config.resolve.alias = {
      ...config.resolve.alias,
      "@": path.resolve(__dirname, "../"),
    };

    // Fix PostCSS configuration for Tailwind CSS v4
    // Prevent Vite from loading postcss.config.mjs by providing inline config
    const tailwindcss = await import("@tailwindcss/postcss");

    config.css = config.css || {};
    config.css.postcss = {
      plugins: [tailwindcss.default()],
    };

    // Enable automatic JSX runtime for React
    config.esbuild = config.esbuild || {};
    config.esbuild.jsx = "automatic";

    // Define global process.env for Next.js compatibility
    config.define = config.define || {};
    const publicEnvVars = Object.entries(process.env).reduce(
      (acc, [key, value]) => {
        if (key.startsWith("NEXT_PUBLIC_")) {
          acc[key] = JSON.stringify(value ?? "");
        }
        return acc;
      },
      {}
    );
    config.define["process.env"] = {
      NODE_ENV: JSON.stringify(process.env.NODE_ENV ?? "development"),
      ...publicEnvVars,
    };

    return config;
  },

  docs: {
    autodocs: "tag",
  },
};

module.exports = config;
