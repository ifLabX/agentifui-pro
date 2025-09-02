import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    // Set workspace root to resolve monorepo lockfile warning
    root: require("path").resolve(__dirname, "../"),
  },
};

// Conditionally enable bundle analyzer (only when not using Turbopack)
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true" && !process.env.TURBOPACK,
});

// Use Turbopack mode when TURBOPACK env var is set, otherwise use standard mode with bundle analyzer
export default process.env.TURBOPACK
  ? nextConfig
  : withBundleAnalyzer(nextConfig);
