import { NextResponse, type NextRequest } from "next/server";

export function middleware(_request: NextRequest) {
  const response = NextResponse.next();

  // Essential security headers for all environments
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  try {
    if (process.env.NODE_ENV === "production") {
      const nonce = Buffer.from(crypto.randomUUID()).toString("base64");

      // Environment variables with defaults
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const allowedOrigins = process.env.NEXT_PUBLIC_ALLOWED_ORIGINS || "";

      // Warn if production environment uses localhost
      if (apiUrl.includes("localhost") || apiUrl.includes("127.0.0.1")) {
        console.warn(
          "🚨 Production environment using localhost API URL:",
          apiUrl
        );
      }

      // Parse allowed origins (handle comma-separated string)
      const originsList = allowedOrigins
        ? allowedOrigins
            .split(",")
            .map(origin => origin.trim())
            .filter(Boolean)
        : [];

      // Production: strict origins only, NO localhost wildcards
      const allowedConnections = ["'self'", apiUrl, ...originsList]
        .filter(Boolean)
        .join(" ");

      const csp = `
        default-src 'self';
        script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
        style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
        connect-src ${allowedConnections};
        img-src 'self' data: blob: https:;
        font-src 'self' https://fonts.gstatic.com;
        object-src 'none';
        base-uri 'self';
        form-action 'self';
        upgrade-insecure-requests;
      `
        .replace(/\s+/g, " ")
        .trim();

      response.headers.set("Content-Security-Policy", csp);
      response.headers.set(
        "Strict-Transport-Security",
        "max-age=31536000; includeSubDomains"
      );
    } else {
      // Development: allow localhost for dev server
      const devConnections = [
        "'self'",
        "http://localhost:*",
        "http://127.0.0.1:*",
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
      ]
        .filter(Boolean)
        .join(" ");

      const devCsp = `
        default-src 'self';
        script-src 'self' 'unsafe-eval' 'unsafe-inline';
        style-src 'self' 'unsafe-inline';
        connect-src ${devConnections};
        img-src 'self' data: blob: https:;
        font-src 'self' https://fonts.gstatic.com;
        object-src 'none';
      `
        .replace(/\s+/g, " ")
        .trim();

      response.headers.set("Content-Security-Policy", devCsp);
    }
  } catch (error) {
    // Only log detailed errors in development
    if (process.env.NODE_ENV !== "production") {
      console.error("Middleware error while generating CSP:", error);
    }
    // Fallback: minimal CSP with basic security headers already set above
    response.headers.set(
      "Content-Security-Policy",
      "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    );
  }

  return response;
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};
