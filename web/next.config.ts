import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

const nextConfig: NextConfig = {
  reactCompiler: true,
  turbopack: {
    // Set workspace root to resolve monorepo lockfile warning
    root: require("path").resolve(__dirname, "../"),
  },
};

// Bundle analyzer is only compatible with Webpack builds
// To use: ANALYZE=true pnpm build (Turbopack not supported)
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true" && !process.env.TURBOPACK,
});

export default withNextIntl(withBundleAnalyzer(nextConfig));
