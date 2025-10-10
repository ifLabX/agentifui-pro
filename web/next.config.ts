import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

const nextConfig: NextConfig = {
  turbopack: {
    // Set workspace root to resolve monorepo lockfile warning
    root: require("path").resolve(__dirname, "../"),
  },
  // Production optimizations: remove console logs except errors
  // Note: This only works with Webpack, not Turbopack
  ...(process.env.NODE_ENV === "production" && {
    compiler: {
      removeConsole: {
        exclude: ["error", "warn"], // Keep console.error and console.warn in production
      },
    },
  }),
};

// Bundle analyzer is only compatible with Webpack builds
// To use: pnpm analyze
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});

export default withNextIntl(withBundleAnalyzer(nextConfig));
